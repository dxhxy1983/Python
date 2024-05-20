nameList=["腔体材质","尺寸","过渡腔室","靶枪数量","靶枪类型",
            "靶枪尺寸","靶枪方向","电源类型","偏置电压","离子源",
            "前级泵","次级泵","抽速1","抽速2","样品台尺寸",
            "样品台旋转功能","样品台温控","样品台升降距离",
            "样品台挡板","流量计数量","气体种类","量程",
            "膜厚仪数量","膜厚仪品牌",]
for item in nameList:
    print(""" [Column("{0}")]
 public string? {0} {1}
    """.format(item,str("{"+"get; set;"+"}")))
for item in nameList:
    print("""entity.Property(e => e.{0}).HasColumnName("{0}").HasMaxLength(100);""".format(item))
