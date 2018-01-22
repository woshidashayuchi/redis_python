# -*- coding: utf-8 -*-
# Author: bill-jack<xfwangaw@isoftstone.com>

import redis

# 配置连接池信息
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)

# 连接连接池
r = redis.Redis(connection_pool=pool)

def string_op():
    '''
     总体说明：
     set();
     mset();
     get(name);
     mget(keys, *args);
     getset(name, value)
     getrange(key, start, end)
     setrange(name, offset, value)
     setbit(name, offset, value)
     getbit(name, offset)
     bitcount(key, start=None, end=None)
     strlen(name)
     incr(self, name, amount=1)
     incrbyfloat(self, name, amount=1.0)
     decr(self, name, amount=1)
     append(name, value)'''
    # 在Redis中设置值，默认不存在则创建，存在则修改
    r.set('Name','test')
    '''参数：
     set(name, value, ex=None, px=None, nx=False, xx=False)
     ex，过期时间（秒）
     px，过期时间（毫秒）
     nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
     xx，如果设置为True，则只有name存在时，当前set操作才执行'''
    
    # 批量设置
    r.mset(name1='zhangsan', name2='lisi')
    # 或
    r.mset({'name1': 'zhangsan','name2': 'lisi'})

    # 批量获取
    print r.mget('name1', 'name2')
    # 或
    li = ['name1', 'name2']
    print r.mget(li)

    # 设置新值，打印原值
    print(r.getset("name1","wangwu")) #输出:zhangsan
    print(r.get("name1")) #输出:wangwu
    
    # 根据字节获取子序列
    r.set('name3', 'ceshi')
    print r.getrange('name3', 0, 3)
    
    # 修改字符串内容，从指定字符串索引开始向后替换，如果新值太长时，则向后添加
    r.set("name","zhangsan")
    r.setrange("name",1,"z")
    print(r.get("name")) #输出:zzangsan
    r.setrange("name",6,"zzzzzzz")
    print(r.get("name")) #输出:zzangszzzzzzz
    
    #自增mount对应的值，当mount不存在时，则创建mount＝amount，否则，则自增,amount为自增数(整数)
    print r.incr("mount",amount=2) # 输出:2
    print r.incr("mount") # 输出:3
    print r.incr("mount",amount=3) # 输出:6
    print r.incr("mount",amount=6) # 输出:12
    print r.get("mount") # 输出:12

    # 在name对应的值后面追加内容
    r.set("name","zhangsan")
    print(r.get("name"))    #输出:'zhangsan
    r.append("name","lisi")
    print(r.get("name"))    #输出:zhangsanlisi


def hash_op():
    # redis中的Hash 在内存中类似于一个name对应一个dic来存储

    '''
     hset(name, key, value)
     hget(name,key)
     hgetall(name)
     hmset(name, mapping)
     hmget(name, keys, *args)
     hlen(name)、hkeys(name)、hvals(name)
     hexists(name, key)
     hdel(name,*keys)
     hincrby(name, key, amount=1)
     hincrbyfloat(name, key, amount=1.0)'''
    # name对应的hash中设置一个键值对（不存在，则创建，否则，修改）
    r.hset('dict_name', 'a', 'aa')
    
    # 在name对应的hash中根据key获取value
    print r.hget('dict_name', 'a') # 输出aa
    
    # 获取name对应hash的所有键值
    print(r.hgetall("dic_name"))
    
    #在name对应的hash中批量设置键值对,mapping:字典
    dic={"a1":"aa","b1":"bb"}
    r.hmset("dic_name",dic)
    print(r.hget("dic_name","b1"))#输出:bb

    # 在name对应的hash中获取多个key的值
    li=["a1","b1"]
    print(r.hmget("dic_name",li))
    print(r.hmget("dic_name","a1","b1"))
    
    dic={"a1":"aa","b1":"bb"}
    r.hmset("dic_name",dic)

    # hlen(name) 获取hash中键值对的个数
    print(r.hlen("dic_name"))

    # hkeys(name) 获取hash中所有的key的值
    print(r.hkeys("dic_name"))

    # hvals(name) 获取hash中所有的value的值
    print(r.hvals("dic_name"))
    
    # 检查name对应的hash是否存在当前传入的key
    print(r.hexists("dic_name","a1")) #输出:True
    
    # 删除指定name对应的key所在的键值对
    r.hdel("dic_name","a1")

    # 自增hash中key对应的值，不存在则创建key=amount(amount为整数)
    print(r.hincrby("demo","a",amount=2))


def list_op():
    # redis中的List在在内存中按照一个name对应一个List来存储 
    '''
     lpush(name,values)
     rpush(name,values)
     lpushx(name,value)
     rpushx(name,value)
     llen(name)
     linsert(name, where, refvalue, value))
     r.lset(name, index, value)
     r.lrem(name, value, num)
     lpop(name)
     lindex(name, index)
     lrange(name, start, end)
     ltrim(name, start, end)
     rpoplpush(src, dst)
     brpoplpush(src, dst, timeout=0)
     blpop(keys, timeout)
     r.brpop(keys, timeout)'''
    
    # 在name对应的list中添加元素，每个新的元素都添加到列表的最左边
    r.lpush("list_name",2)
    r.lpush("list_name",3,4,5)#保存在列表中的顺序为5，4，3，2
    
    # 在name对应的list中添加元素，每个新的元素都添加到列表的最右边
    r.rpush("list_name", 6)
    # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
    r.lpushx('list_name', 7)
    # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最右边
    r.rpushx('list_name', 8)
    
    # name对应的list元素的个数
    print(r.llen("list_name"))

    # 在name对应的列表的某一个值前或后插入一个新值
    r.linsert("list_name","BEFORE","2","SS")#在列表内找到第一个元素2，在它前面插入SS
    
    '''参数：
     name: redis的name
     where: BEFORE（前）或AFTER（后）
     refvalue: 列表内的值
     value: 要插入的数据'''

    # 对list中的某一个索引位置重新赋值
    r.lset("list_name",0,"bbb")

    # 删除name对应的list中的指定值
    r.lrem("list_name","SS",num=0)

    ''' 参数：
    name:  redis的name
    value: 要删除的值
    num:   num=0 删除列表中所有的指定值；
           num=2 从前到后，删除2个；
           num=-2 从后向前，删除2个'''

    # 移除列表的左侧第一个元素，返回值则是第一个元素
    print(r.lpop("list_name"))

    # 根据索引获取列表内元素
    print(r.lindex("list_name",1))

    # 分片获取元素
    print(r.lrange("list_name",0,-1))

    # 移除列表内没有在该索引之内的值
    r.ltrim("list_name",0,2)
    
    # 同rpoplpush，多了个timeout, timeout：取数据的列表没元素后的阻塞时间，0为一直阻塞,timeout可没有
    r.brpoplpush("list_name","list_name1",timeout=1)
    
    # 将多个列表排列,按照从左到右去移除各个列表内的元素
    r.lpush("list_name",3,4,5)
    r.lpush("list_name1",3,4,5)

    # while True:
    #     print(r.blpop(["list_name","list_name1"],timeout=1))
    #     print(r.lrange("list_name",0,-1),r.lrange("list_name1",0,-1))

    '''keys: redis的name的集合
         timeout: 超时时间，获取完所有列表的元素之后，阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞'''


def set_op():
    # Set集合就是不允许重复的列表
    '''
     sadd(name,values)
     smembers(name)
     scard(name)
     sdiff(keys, *args)
     sdiffstore(dest, keys, *args)
     sinter(keys, *args)
     sinterstore(dest, keys, *args)
     sismember(name, value)
     smove(src, dst, value)
     spop(name)
     srandmember(name, numbers)
     srem(name, values)
     sunion(keys, *args)
     sunionstore(dest,keys, *args)'''
    # 给name对应的集合中添加元素
    r.sadd("set_name","aa")
    r.sadd("set_name","aa","bb")
    
    # 获取name对应的集合的所有成员
    members = r.smembers('set_name')
    print members
    # 获取name对应的集合中的元素个数
    scard = r.scard('set_name')
    print scard
    
    #在第一个name对应的集合中且不在其他name对应的集合的元素集合
    r.sadd("set_name","aa","bb")
    r.sadd("set_name1","bb","cc")
    r.sadd("set_name2","bb","cc","dd")
    print(r.sdiff("set_name","set_name1","set_name2"))#输出:｛aa}
    
    # 相当于把sdiff获取的值加入到dest对应的集合中
    r.sdiffstore("new_set","set_name","set_name1","set_name2")

    # 获取多个name对应集合的并集
    r.sadd("set_name","aa","bb")
    r.sadd("set_name1","bb","cc")
    r.sadd("set_name2","bb","cc","dd")
    print(r.sinter("set_name","set_name1","set_name2"))#输出:｛bb｝
    
    #获取多个name对应集合的并集，再讲其加入到dest对应的集合中
    print r.sinterstore("new_new_set","set_name","set_name1","set_name2")

    # 检查value是否是name对应的集合内的元素
    print r.sismember("set_name", "aa")
    
    # 将某个元素从一个集合中移动到另外一个集合
    # smove(src, dst, value)
    
    #从集合的右侧移除一个元素，并将其返回
    # spop(name)
    
    # 从name对应的集合中随机获取numbers个元素
    print(r.srandmember("set_name2",2))

    #删除name对应的集合中的某些值
    print(r.srem("set_name2","bb","dd"))

    #获取多个name对应的集合的并集
    print r.sunion("set_name","set_name1","set_name2")

    #获取多个name对应的集合的并集，并将结果保存到dest对应的集合中
    print r.sunionstore('dest_set',"set_name","set_name1","set_name2")


def z_set_op():
    # 在集合的基础上，为每元素排序，元素的排序需要根据另外一个值来进行比较，所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。
    '''
     zadd(name, *args, **kwargs)
     zcard(name)
     zcount(name, min, max)
     zincrby(name, value, amount)
     zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)
     zrevrange(name, start, end, withscores=False, score_cast_func=float)
     zrank(name, value)、zrevrank(name, value)
     zscore(name, value)
     zrem(name, values)
     zremrangebyrank(name, min, max)
     zremrangebyscore(name, min, max)
     zinterstore(dest, keys, aggregate=None)
     zunionstore(dest, keys, aggregate=None)
     '''
    # 在name对应的有序集合中添加元素
    r.zadd("zset_name", "a1", 6, "a2", 2,"a3",5)
    # 或
    r.zadd('zset_name1', b1=10, b2=5)
    
    #获取有序集合内元素的数量
    print r.zcard('zset_name1')
    
    #获取有序集合中分数在[min,max]之间的个数
    print(r.zcount("zset_name",1,5))

    #自增有序集合内value对应的分数
    r.zincrby("zset_name","a1",amount=2)#自增zset_name对应的有序集合里a1对应的分数

    # 按照索引范围获取name对应的有序集合的元素
    aa=r.zrange("zset_name",0,1,desc=False,withscores=True,score_cast_func=int)
    print(aa)
    '''参数：
        name    redis的name
        start   有序集合索引起始位置
        end     有序集合索引结束位置
        desc    排序规则，默认按照分数从小到大排序
        withscores  是否获取元素的分数，默认只获取元素的值
        score_cast_func 对分数进行数据转换的函数'''

    
if __name__ == '__main__':
    '''
     delete(*names)
    根据name删除redis中的任意数据类型

    exists(name)
    检测redis的name是否存在

    keys(pattern='*')
    根据* ？等通配符匹配获取redis的name
    
    expire(name ,time)
    为某个name设置超时时间

    rename(src, dst)
    # 重命名

    move(name, db))
    # 将redis的某个值移动到指定的db下
    
    randomkey()
    #随机获取一个redis的name（不删除）

    type(name)
    # 获取name对应值的类型'''
    # zadd(name, *args, **kwargs)在name对应的有序集合中添加元素
    r.zadd('hello','d',2,'b',1,'c',3)

    # 按照索引范围获取name对应的有序集合的元素
    n = r.zrange('hello',0, 5, desc=False, withscores=True, score_cast_func=str)
    print n
    
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
    # 检查redis的name是否存在
    print (r.exists('hello'))

    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    # 为某个redis的某个name设置超时时间（秒
    r.expire('hello',20)

    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    # type(name)获取name对应值的类型
    print r.type('hello')
    
    string_op()
    hash_op()
    list_op()
    set_op()
