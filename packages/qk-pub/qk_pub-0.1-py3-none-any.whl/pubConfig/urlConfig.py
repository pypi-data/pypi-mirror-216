##料箱车容器搬运接口
sendContainerMoveUrl_281 = "http://{}:9001/api/rcs/warehouse/{}/workbin/job/workbin_move"
sendContainerMoveUrl_290 = "http://{}:9001/api/rcs/warehouse/{}/workbin/job/workbin_move"

##青鸾车容器搬运接口
sendQLContainerMoveUrl_291 = "http://{}:9001/api/rcs/warehouse/{}/carrier/job/ql_container_move"

##聚灵wms入库单接口
jl_wms_warehouse_order_url = "http://{}/kc_agv/ws/platBaseService/invoke/winit2sis_replenish_push"
jl_wms_container_update_url = "http://{}/kc_agv/ws/platBaseService/invoke/s_swms_wcs_kc_common"

##释放货位锁闭接口
releaseSlotLockUrl_291 = "http://{}:9001/api/rcs/warehouse/1/bucket/slotLock"

##错误码导入接口
errorNoReportUrl = "http://{}:9001/api/rcs/dsp/importData/{}"

# 单夹抱货位/料箱盘点任务接口
workBinTryDecodeJobUrl_291 = "http://{}:9001/api/rcs/warehouse/{}/workbin/job/workbin_verify"
