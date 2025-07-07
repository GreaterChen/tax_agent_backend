from typing import Dict, Optional
from fastapi import Request


class NewsTypeUtil:
    """
    新闻类别多语言工具类
    """
    
    # 新闻类别多语言映射
    NEWS_TYPE_MAPPING = {
        'Legislation': {
            'en': 'Legislation',
            'zh-cn': '立法动态',
            'zh-tw': '立法動態'
        },
        'Policy': {
            'en': 'Policy',
            'zh-cn': '政策',
            'zh-tw': '政策'
        },
        'HKICPA': {
            'en': 'HKICPA',
            'zh-cn': 'HKICPA',
            'zh-tw': 'CKICPA'
        },
        'ACCA': {
            'en': 'ACCA',
            'zh-cn': 'ACCA',
            'zh-tw': 'ACCA'
        },
        'Industry': {
            'en': 'Industry',
            'zh-cn': '行业动态',
            'zh-tw': '行業動態'
        }
    }
    
    @classmethod
    def get_language_from_request(cls, request: Request) -> str:
        """
        从请求头中获取语言信息
        
        :param request: FastAPI Request对象
        :return: 语言代码
        """
        accept_language = request.headers.get('Accept-Language', 'en')
        
        # 解析Accept-Language头，获取首选语言
        if 'zh-cn' in accept_language.lower() or 'zh-hans' in accept_language.lower():
            return 'zh-cn'
        elif 'zh-tw' in accept_language.lower() or 'zh-hant' in accept_language.lower():
            return 'zh-tw'
        elif 'zh' in accept_language.lower():
            return 'zh-cn'  # 默认简体中文
        else:
            return 'en'
    
    @classmethod
    def get_news_type_display(cls, news_type: str, language: str) -> str:
        """
        根据新闻类别和语言获取显示文本
        
        :param news_type: 新闻类别代码
        :param language: 语言代码
        :return: 显示文本
        """
        if news_type in cls.NEWS_TYPE_MAPPING:
            return cls.NEWS_TYPE_MAPPING[news_type].get(language, news_type)
        return news_type
    
    @classmethod
    def get_news_type_display_from_request(cls, news_type: str, request: Request) -> str:
        """
        根据新闻类别和请求获取显示文本
        
        :param news_type: 新闻类别代码
        :param request: FastAPI Request对象
        :return: 显示文本
        """
        language = cls.get_language_from_request(request)
        return cls.get_news_type_display(news_type, language)
    
    @classmethod
    def get_all_news_types(cls) -> Dict[str, Dict[str, str]]:
        """
        获取所有新闻类别及其多语言映射
        
        :return: 新闻类别映射字典
        """
        return cls.NEWS_TYPE_MAPPING
    
    @classmethod
    def get_news_type_keys(cls) -> list:
        """
        获取所有新闻类别的键
        
        :return: 新闻类别键列表
        """
        return list(cls.NEWS_TYPE_MAPPING.keys()) 