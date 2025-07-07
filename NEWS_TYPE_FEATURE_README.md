# 新闻类别功能说明

## 功能概述

为news模块新增了`newsType`字段，支持多语言的新闻类别显示。系统会根据请求头中的`Accept-Language`信息返回对应语言的类别文字。

## 支持的新闻类别

| 类别代码 | 英文 | 简体中文 | 繁体中文 |
|---------|------|----------|----------|
| Legislation | Legislation | 立法动态 | 立法動態 |
| Policy | Policy | 政策 | 政策 |
| HKICPA | HKICPA | HKICPA | CKICPA |
| ACCA | ACCA | ACCA | ACCA |
| Industry | Industry | 行业动态 | 行業動態 |

## 数据库变更

### 1. 执行SQL迁移脚本

**MySQL数据库：**
```sql
-- 添加news_type字段
ALTER TABLE news ADD news_type VARCHAR(50) DEFAULT NULL;

-- 创建索引以提高查询性能
CREATE INDEX idx_news_type ON news(news_type);
```

**PostgreSQL数据库：**
```sql
-- 添加news_type字段
ALTER TABLE news ADD COLUMN news_type VARCHAR(50) DEFAULT NULL;

-- 添加列注释
COMMENT ON COLUMN news.news_type IS '新闻类别';

-- 创建索引以提高查询性能
CREATE INDEX idx_news_type ON news(news_type);
```

## API变更

### 1. 新增字段

**请求和响应模型中新增字段：**
- `newsType`: 新闻类别代码（存储在数据库中）
- `newsTypeDisplay`: 新闻类别显示文本（根据语言动态生成）

### 2. 新增接口

**获取新闻类别选项：**
```
GET /system/news/newsTypes
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": [
    {
      "value": "Legislation",
      "label": "立法动态"
    },
    {
      "value": "Policy", 
      "label": "政策"
    },
    ...
  ]
}
```

### 3. 现有接口增强

所有现有的新闻接口都已增强，会根据请求头返回对应语言的类别显示：

- `GET /system/news/list` - 新闻列表
- `GET /system/news/{id}` - 新闻详情
- `POST /system/news/export` - 导出新闻

## 多语言支持

系统根据请求头中的`Accept-Language`信息自动判断语言：

- `zh-cn`, `zh-hans` -> 简体中文
- `zh-tw`, `zh-hant` -> 繁体中文  
- `zh` -> 简体中文（默认）
- 其他 -> 英文

## 使用示例

### 1. 创建新闻时指定类别

```json
{
  "title": "最新政策发布",
  "content": "政策内容...",
  "newsType": "Policy"
}
```

### 2. 查询指定类别的新闻

```
GET /system/news/list?newsType=Policy
```

### 3. 设置请求头获取中文显示

```
Accept-Language: zh-cn
```

响应中`newsTypeDisplay`字段将显示为"政策"。

## 技术实现

### 1. 多语言工具类

`utils/news_type_util.py` - 负责处理多语言转换逻辑

### 2. 核心文件修改

- `module_admin/entity/do/news_do.py` - 数据库模型
- `module_admin/entity/vo/news_vo.py` - 接口模型
- `module_admin/dao/news_dao.py` - 数据访问层
- `module_admin/service/news_service.py` - 业务逻辑层
- `module_admin/controller/news_controller.py` - 控制器层

### 3. 关键特性

- 存储时使用英文代码，节省存储空间
- 显示时根据语言动态转换
- 支持查询条件过滤
- 导出功能包含多语言支持
- 新增专门的类别选项接口

## 注意事项

1. 数据库中存储的是类别代码（如"Policy"），不是显示文本
2. 前端应使用`newsTypeDisplay`字段显示给用户
3. 查询时仍需使用`newsType`字段（代码）进行过滤
4. 建议在前端缓存类别选项，避免重复请求 