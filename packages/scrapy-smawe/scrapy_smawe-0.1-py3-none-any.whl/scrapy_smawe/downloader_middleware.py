class DefineDownloaderMiddleware:
    """定义DownloaderMiddleware需要定义以下方法之一."""

    def process_request(self, request, spider):
        """
        DownloaderMiddleware调用优先级越小, 此方法越先被调用
        :param request: Request object, 即被处理的Request
        :param spider: Spider object, 即此Request对应的Spider对象
        :return:
            1. 当返回None时, scrapy继续处理该Request, 接着执行其它DownloaderMiddleware的process_request方法
            2. 当返回Response对象时, 更低优先级的DownloaderMiddleware的process_request和process_exception方法不会被继续调用
            每个DownloaderMiddleware的process_response方法依次被调用(调用优先级从大到小)
            3. 当返回Request对象时, 更低优先级的DownloaderMiddleware的process_request方法会暂停执行, 这个Request会被重新放入调度队列
        """

    def process_response(self, request, response, spider):
        """
        DownloaderMiddleware调用优先级越大, 此方法越先被调用
        :param request: Request object, 即此Response对应的Request
        :param response: Response object, 即被处理的Response
        :param spider: Spider object, 即此Response对应的Spider对象
        :return:
            1. 当返回Request对象时, 更低优先级的DownloaderMiddleware的process_response方法不会继续被调用.
            该Request对象会重新放入调度队列里
            2. 当返回Response对象时, 更低优先级的DownloaderMiddleware的process_response方法会继续被调用
            3. 如果抛出IgnoreRequest异常, 则Request的errorback方法会回调, 如果该异常还没有被处理, 那么它会被忽略.
        """

    def process_exception(self, request, exception, spider):
        """
        process_request方法抛出IgnoreRequest异常时, 会调用次方法.
        :param request: Request object, 即产生异常的Request
        :param exception: Exception object, 即抛出的异常
        :param spider: Spider object, 即Request对应的Spider
        :return:
            1. 当返回为None时, 更低优先级的DownloaderMiddleware的process_exception方法会依次被调用(调用优先级从大到小)
            2. 当返回为Response对象时, 更低优先级的DownloaderMiddleware的process_exception方法不再被继续调用,
            每个DownloaderMiddleware的process_response方法依次被调用(调用优先级从大到小)
            3. 当返回Request对象时, 更低优先级的DownloaderMiddleware的process_exception方法也不再被继续调用,
            该Request对象会重新被放入到调度队列里.
        """
