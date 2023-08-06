class DefineSpiderMiddleware:
    """定义SpiderMiddleware需要定义以下方法之一"""

    def process_spider_input(self, response, spider):
        """
        处理scrapy从downloader发送过来的response.
        :param response: Response对象, 即被处理的Response
        :param spider: Response对应的Spider对象
        :return:
            1. 当返回是None时, 继续执行其它SpiderMiddleware(调用优先级从小到大)
            2.
                (1). 当发生异常时, 如果Response对象对应的Request对象有绑定错误处理回调, 则调同此回调,
                    然后将回调输出从SpiderMiddleware的另一端输入, 然后继续执行process_spider_output方法(调用优先级从大到小)
                (2). 当发生异常时, 如果Response对象对应的Request对象没有绑定错误处理回调, 则调用process_spider_exception方法(调用优先级从大到小)

        """

    def process_spider_output(self, response, result, spider):
        """
        处理Spider解析完后的response, 在发送到Engine之前执行
        :param response: 生成该输出的Response对象
        :param result: 一个包含Request或Item对象的可迭代对象
        :param spider:  Response对应的Spider对象
        :return: 必须返回包含Request或Item对象的可迭代对象
        """

    def process_spider_exception(self, response, exception, spider):
        """
        处理process_spider_input发生的异常
        :param response: Response对象, 即抛出异常时被处理的response
        :param exception: Exception对象, 即抛出的异常
        :param spider: Response对应的Spider对象
        :return:
            1. 当返回为None时, 继续执行其它SpiderMiddleware的process_spider_exception方法
            2. 当返回为一个包含Request或Item对象的可迭代对象时, 则从当前的下一个SpiderMiddleware的process_spider_output方法开始
                必须返回一个包含Requests或Item对象的可迭代对象(调用优先级从大到小), 且只会执行一次调用优先级最小的process_spider_output
                方法.
        """

    def process_start_requests(self, start_requests, spider):
        """
        处理从Spider中获取的初始请求(调用优先级从小到大依次执行)
        :param start_requests: 包含Request的可迭代对象, 即Start Requests
        :param spider: Spider对象, 即Start Requests所属的Spider
        :return: 必须返回另一个包含Request对象的可迭代对象
        """
