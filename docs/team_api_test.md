# 组队活动接口测试说明（#38）

> 对应 Issue：#38 组队活动修改、删除与状态管理接口
> 测试环境：本机无 SQL Server 与 InterestDB，采用 Flask `test_client` + 内存桩连接执行
> 结论：桩验证通过；标“待真库复验”的用例需在有数据库的机器上重跑

## 1. 用例与结果

| 编号 | 接口 | 场景 | 预期 | 结果 |
|---|---|---|---|---|
| TC-01 | PUT /api/activities/{id} | 未携带 token | 401 未登录或登录已过期 | 通过 |
| TC-02 | PUT /api/activities/{id} | 非创建者修改 | 403 无权操作该活动 | 通过 |
| TC-03 | PUT /api/activities/{id} | 活动 ID 不存在 | 404 活动不存在 | 通过 |
| TC-04 | PUT /api/activities/{id} | 人数上限改为 1，当前报名 2 人 | 400 人数上限不能小于当前报名人数（2） | 通过 |
| TC-05 | PUT /api/activities/{id} | 只提交标题 | 200 修改成功，其余字段保持原值 | 通过 |
| TC-06 | PUT /api/activities/{id} | status 置为已关闭 | 200 修改成功，返回 status=已关闭 | 通过 |
| TC-07 | PUT /api/activities/{id} | 活动已关闭后再修改 | 409 活动已关闭，不能修改 | 通过 |
| TC-08 | PUT /api/activities/{id} | 招募中活动传 status=满员 | 400 活动状态只能为：招募中、已关闭 | 通过 |
| TC-09 | PUT /api/activities/{id} | 人数上限改为等于报名人数 | 200 修改成功 | 通过 |
| TC-10 | DELETE /api/activities/{id} | 非创建者删除 | 403 无权操作该活动 | 通过 |
| TC-11 | DELETE /api/activities/{id} | 创建者删除 | 200 删除成功，报名记录同步清除 | 通过 |
| TC-12 | DELETE /api/activities/{id} | 未携带 token | 401 未登录或登录已过期 | 通过 |
| TC-13 | POST /api/activities | 缺少人数上限 | 400 人数上限必须为正整数 | 通过 |
| TC-14 | POST /api/activities | 缺少标题 | 400 活动标题不能为空 | 通过 |
| TC-15 | PUT /api/activities/{id} | 人数上限传布尔值或小数 | 400 人数上限必须为正整数 | 通过 |

## 2. 待真库复验

| 项 | 原因 |
|---|---|
| 列表、详情接口未回归 | 桩连接只覆盖改删路径，需连真实库确认排序与报名人数统计 |
| 删除时外键顺序 | 已按先删报名、后删活动的顺序执行，需在 SQL Server 上确认事务与外键无冲突 |
| 中文状态写入 | 需确认 Status 字段 N 前缀与默认值在真实库中生效 |
