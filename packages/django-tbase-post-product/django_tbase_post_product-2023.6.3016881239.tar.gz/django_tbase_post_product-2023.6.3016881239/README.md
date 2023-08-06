# django-expand/tbase_post_product

用于产品的文章模块



安装
```bash
pip install django-tbase-post-product
```

```python
# settings.py
 INSTALLED_APPS = [   # 个人应用
     # 基本配置
    # 'tbase_page',
    'tbase_config',
    'tbase_theme_tailwind',
    
    'tbase_post',
    # 'markdownx'
    'martor',
    'taggit',

 ]
```


## 更新

- 2023/06/05
优化相关内容查询,模板文件,针对tags内容数目低于10的链接添加nofollow。


- 2023/06/02
加入seo优化，对tags内容过少（小于10）的页面添加noindex






## Getting Started

Download links:

SSH clone URL: ssh://git@git.jetbrains.space/terrychanorg/django-expand/tbase_post_product.git

HTTPS clone URL: https://git.jetbrains.space/terrychanorg/django-expand/tbase_post_product.git



These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software and how to install them.

```
Examples
```

## Deployment

Add additional notes about how to deploy this on a production system.

## Resources

Add links to external resources for this project, such as CI server, bug tracker, etc.
