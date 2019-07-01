# todolist
Argon Design 的 Todo List 工具，刷题的得力伙伴

### Feature

1. 简洁清爽的 UI ，使用现代感十足的 Argon Design 框架
2. 在浏览器中打开并编辑 Todo List ，而不是像 memset0 之前那个项目一样需要弱智般得手改配置文件
3. 支持常见的各大 OJ ，现在已有 UOJ / LOJ / BZOJ ，将会马上添加洛谷 / CF / Vjudge
4. 支持获取其他网友的做题记录并进行比较，也可以用于机房的题目交流

### Usage

安装 [Python3](https://www.baidu.com/s?wd=安装python3教程) 和 [git](https://www.baidu.com/s?wd=安装git教程) 环境，在空目录下运行命令

```shell
git clone https://github.com/memset0/todolist .
pip3 install -r requirements.txt
cp user.sample.yml user.yml
cp config.sample.yml config.yml
cp problem.sample.yml problem.yml
python3 server.py
```

配置 `user.yml`, `config.yml`, `problem.yml` 后打开 [localhost:23333](http://localhost:23333) 。

### Todo

按计划完成的顺序排序

* BZOJ 的权限题爬取
  * 一个方案是做成一个共用的 api 放网上供调用，缺点是成本比较高。
  * 另一个方案是把爬好的题目内容放在 `problem_list.yml` 里，缺点是可能不能及时更新新的权限题（搞得好像 BZOJ 在更新新的权限题似的
  * 现在的解决方案是你可以在 `config.yml` 中填写权限号的 cookies 来达到爬取权限号题目名称的效果
* 洛谷的题目名称和做题记录爬取
* CodeForces 的题目名称和做题记录爬取
* VJudge 的题目名称和做题记录爬取