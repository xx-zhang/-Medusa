> 目前已知问题

- **FastJson**只可扫描`www.ascotbe.com:12345`或者`www.ascotbe.com`这样域名下的漏洞，无法扫描`www.ascotbe.com/aaaa/XXXXX`这类目录下漏洞（后续代理扫描可以扫到
- 枚举多端口后异步扫描（后续添加
- 枚举子域名后异步扫描（后续添加
- 多级目录探测（由于多线程容易造成DOS暂时关闭