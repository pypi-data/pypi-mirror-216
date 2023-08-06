from typing import List, Union

import pandas as pd
import requests

from sj_tool.fjsp.erp_next.util import connect_erp_db, get_http_header, update_table, select_data_from_table


# def lock_sale_orders(order_ids:  Union[str,List[str]], owner=str):
#     _lock_unlock_sale_orders(order_ids,True)
# def unlock_sale_orders(order_ids: Union[str,List[str]]):
#     _lock_unlock_sale_orders(order_ids,False)


def lock_unlock_sale_orders_by_http(order_ids: Union[str, List[str]], lock: bool, owner: str):
    if isinstance(order_ids, str):
        order_ids = [order_ids]
    headers = get_http_header()
    table_name = "Sales Order Item"
    fields = ["name", "item_code", "locked"]
    fields_str = str(fields)[1:-1].replace("'", '"')

    for order_item_id in order_ids:
        item_id = order_item_id[order_item_id.rfind("-"):]
        update_url = f"http://192.168.50.73/api/resource/{table_name}/{item_id}"
        res = requests.put(update_url, headers=headers, data={"locked": 1 if lock else 0})


def lock_unlock_sale_orders_by_http_with_query(order_ids: Union[str, List[str]], lock: bool, owner: str):
    if isinstance(order_ids, str):
        order_ids = [order_ids]
    headers = get_http_header()
    table_name = "Sales Order Item"
    fields = ["name", "item_code", "locked"]
    fields_str = str(fields)[1:-1].replace("'", '"')

    for order_item_id in order_ids:
        item_id = order_item_id[order_item_id.rfind("-"):]
        filters = [("name", item_id), ("owner", owner)]
        fileter_str = str([[table_name, f[0], "=", f[1]] for f in filters]).replace("'", '"')
        if len(filters) > 0:
            query_url = f"http://192.168.50.73/api/resource/{table_name}?fields=[{fields_str}]&&filters={fileter_str}"
        else:
            query_url = f"http://192.168.50.73/api/resource/{table_name}?fields=[{fields_str}]"

        res = requests.get(query_url, headers=headers)
        print(res.text)

        update_url = f"http://192.168.50.73/api/resource/{table_name}/{item_id}"
        res = requests.put(update_url, headers=headers, data={"locked": 1 if lock else 0})


def lock_unlock_sale_orders(order_ids: Union[str, List[str]], lock: bool, owner: str):
    if isinstance(order_ids, str):
        order_ids = [order_ids]
    table_name = "tabSales Order Item"

    conn = connect_erp_db()
    for order_item_id in order_ids:
        item_id = order_item_id[order_item_id.rfind("-") + 1:]
        update_table(conn, table_name, {"locked": 1 if lock else 0}, f"name='{item_id}'")

    conn.close()


def lock_on_way_inv(part_number, lock_qty, if_on_hand, mad=None, owner="1091076149@qq.com"):
    conn = connect_erp_db()
    table_name = "tabPurchase Order Item"
    fields = ["name", "item_code", "qty", "schedule_date", "lock_qty"]

    # 查询物料
    results = []
    tmp_data = select_data_from_table(
        conn,
        table_name,
        columns=fields,
        where_clause=f"owner = %s and item_code = %s" if if_on_hand else f"owner = %s and item_code = %s and schedule_date = %s",
        where_params=(owner, part_number) if if_on_hand else (owner, part_number, mad),
    )
    for row in tmp_data:
        results.append(
            {"name": row["name"], "item_code": row["item_code"], "qty": row["qty"],
             "schedule_date": row["schedule_date"], "lock_qty": row["lock_qty"]}
        )
    results = pd.DataFrame(results)

    # 锁定期初库存
    for idx, row in results.sort_values(by=["schedule_date"]).iterrows():
        if lock_qty == 0:
            break
        qty = row["qty"]
        locked_qty = row["lock_qty"]
        idx = row["name"]
        tmp = min(qty - locked_qty, lock_qty)
        update_table(conn, table_name, {"lock_qty": tmp}, f"name='{idx}'")
        lock_qty -= tmp
    if lock_qty != 0:
        raise Exception(part_number + " lock error, if_on_hand: " + str(if_on_hand))
    conn.close()


if __name__ == "__main__":
    # lock_unlock_sale_orders("fp_SIZE_4222241773_L420-000030-00086916d5", True, owner="1091076149@qq.com")
    lock_on_way_inv("SD10M34154", 5000, True)
