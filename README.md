# **WZU在线判题系统acm.wzu.edu.cn实验报告生成器**


### **写该脚本的初衷是为了节约生命**


## **配置**

cookie值

判题系统中AC题目的url(自行获取替换到108行,去掉page的值，到111行配置pageNum即为AC结果页面的页面总数，46行同)

实验报告生成页面的url(109行,题目编号用{}替换)

课程号(20行，109)

题目编号开头(23行)

实验地址(25行)

老师名字(39行)

如需要生成作业自己修改target_url_template的url

## **使用**

配置好后直接运行，在当前目录下的pdfs/中生成报告

有一个逻辑问题就是无法区分，实验和作业，统一按实验生成实验报告。
若有区别需求的请自行分拣。

deduplication.py #用于多次AC的题目生成报告去重，默认取第一次

