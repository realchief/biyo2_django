select category_id, sum(price*quantity) as sales, sum(quantity) as amount, sum(discount) as discount from
(SELECT
    `{orderitem_tbl}`.`id`,
    `{orderitem_tbl}`.`price`,
    `{orderitem_tbl}`.`discount`,
    `{orderitem_tbl}`.`product_id`,
    `{orderitem_tbl}`.`quantity`,
    (select p2c.category_id from {product2category_tbl} p2c where p2c.product_id=`{orderitem_tbl}`.`product_id` order by p2c.category_id limit 1) as category_id
FROM `{orderitem_tbl}`
WHERE
    ((`{orderitem_tbl}`.`order_id`) IN (SELECT U0.`id` FROM `{order_tbl}` U0 WHERE ((U0.`open_date` BETWEEN '{open_date}' AND '{close_date}' OR U0.`close_date` BETWEEN '{open_date}' AND '{close_date}')AND U0.`status` = 3 AND NOT (U0.`close_date` > '{close_date}' AND U0.`close_date` IS NOT NULL))) AND NOT (`{orderitem_tbl}`.`void_status` = 1 AND `{orderitem_tbl}`.`void_status` IS NOT NULL))
) as rawdata
group by category_id
