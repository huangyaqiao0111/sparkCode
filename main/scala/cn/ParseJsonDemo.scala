package cn

import java.util.Date
import java.text.SimpleDateFormat

import com.alibaba.fastjson.JSON
import org.apache.spark.sql.SparkSession
import org.apache.log4j.{Level, Logger}


object ParseJsonDemo {

  val time = new Date().getTime
  val directoryDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(time)

  //user first json data
  case class UserJson(distinct_id: String, `time`: String, `type`: String, event: String, project: String, time_free: String, properties: String)

  //user properties json data
  case class UserProp($is_login_id: String, $app_version: String, $ip: String, $user_agent: String, $time: String, brand: String, model: String, version: String, system: String, platform: String, shop_id: String)

  //merge UserJson & UserProp
  case class SdkLog(distinct_id: String, `time`: String, `type`: String, event: String, project: String, time_free: String, $is_login_id: String, $app_version: String, $ip: String, $user_agent: String, $time: String, brand: String, model: String, version: String, system: String, platform: String, shop_id: String, insertTime: String)

  def insertHistoryTableIfNull(sparkSession: SparkSession, insertTab: String, fieldName: String, fromTab: String) = {
    sparkSession.sql(
      s"""
        | insert into ${insertTab}
        |     select
        |         ${fieldName},
        |         from_unixtime(unix_timestamp())
        |     from ${fromTab}
      """.stripMargin)
  }

  def insertIncreaseTableIfNull(sparkSession: SparkSession, insertTab: String, fieldName: String, fromTab: String) = {
    sparkSession.sql(
      s"""
        | insert into ${insertTab}
        |     select
        |         count(${fieldName}),
        |         count(${fieldName}),
        |         count(${fieldName}),
        |         from_unixtime(unix_timestamp())
        |     from ${fromTab}
      """.stripMargin)
  }

  def insertHistoryTableNotNull(sparkSession: SparkSession, insertTab: String, fieldName: String, fromTemTab: String) = {
    sparkSession.sql(
      s"""
        | insert into ${insertTab}
        |   select
        |      ${fieldName},
        |      from_unixtime(unix_timestamp())
        |   from ${fromTemTab} where ${fieldName} not in (select ${fieldName} from ${insertTab})
      """.stripMargin)

  }

  def insertIncreaseTableNotNull(sparkSession: SparkSession, insertTab: String, fieldName: String, fromTab: String) = {
    sparkSession.sql(
      s"""
        | insert into ${insertTab}
        |  select
        |    hoursID.Hid,
        |    daysID.Did,
        |    monthsID.Mid,
        |    from_unixtime(unix_timestamp(),'yyyy-MM-dd HH:mm:ss')
        |  from
        |    (
        |      select
        |        count(${fieldName})  Hid,
        |        from_unixtime(unix_timestamp(),'yyyy-MM-dd HH:mm:00') as t
        |    from ${fromTab}
        |        where insert_time between from_unixtime(unix_timestamp() - 300, 'yyyy-MM-dd HH:mm:ss') and from_unixtime(unix_timestamp() , 'yyyy-MM-dd HH:mm:ss')
        |    ) as hoursID
        |  left outer join
        |    (
        |      select
        |        count(${fieldName}) Did,
        |        from_unixtime(unix_timestamp(),'yyyy-MM-dd HH:mm:00') as t
        |    from ${fromTab}
        |        where insert_time between from_unixtime(unix_timestamp(), 'yyyy-MM-dd 00:00:00') and from_unixtime(unix_timestamp(), 'yyyy-MM-dd HH:mm:ss')
        |    ) as daysID  on daysID.t = hoursID.t
        |  left outer join
        |    (
        |      select
        |        count(${fieldName}) Mid,
        |        from_unixtime(unix_timestamp(),'yyyy-MM-dd HH:mm:00') as t
        |    from ${fromTab}
        |       where insert_time between from_unixtime(unix_timestamp(), 'yyyy-MM-01 00:00:00') and from_unixtime(unix_timestamp(), 'yyyy-MM-dd HH:mm:ss')
        |    ) as monthsID on monthsID.t = hoursID.t
        |
        """.stripMargin)

  }

  def main(args: Array[String]): Unit = {
    //Logger.getLogger("Logger").setLevel(Level.ERROR)
    val sparkSession = SparkSession.builder().appName(this.getClass.getSimpleName).master("local").config("spark.some.config.option", "config-value").getOrCreate()
    sparkSession.conf.set("HADOOP_USER_NAME", "hdfs")
    import sparkSession.implicits._
    val sc = sparkSession.sparkContext
    sc.textFile("file:///home/demo/text.txt").map(lines => {
      // 替换逗号，防止json误判
      val line = lines.replace("(KHTML,", "(KHTML")
      val jo: UserJson = JSON.parseObject(line, classOf[UserJson])
      val ua: UserProp = JSON.parseObject(jo.properties, classOf[UserProp])
      SdkLog(jo.distinct_id, jo.`time`, jo.`type`, jo.event, jo.project, jo.time_free, ua.$is_login_id, ua.$app_version, ua.$ip, ua.$user_agent, ua.$time, ua.brand, ua.model, ua.version, ua.system, ua.platform, ua.shop_id, directoryDate)
    }).repartition(1).toDF().createOrReplaceTempView("tempTab")
    sparkSession.sql("use demo")
    // 查看历史表中有没有数据，判断是否为第一次插入数据
    val hisDataBoo: Boolean = sparkSession.sql("select * from history_data limit 1 ").toDF().collect().isEmpty
    // 将本次数据插入到历史数据表中
    sparkSession.sql(" insert into history_data select * from tempTab ")

    // ----------------------------------------------------------------- 以下是插入用户新增

    // 查出本次一小时内数据的用户ID :因为需求是查看每小时新增的用户以及门店数，所以需要去重id，其他需求则可以在history_data中实现
    sparkSession.sql("select distinct_id from tempTab group by distinct_id having distinct_id is not null ").toDF().createOrReplaceTempView("tempTabDisId")
    // 如果历史表中没有数据，那么其他表中也不会有数据，则本次所查出的distinct_id 全部为新用户
    if (hisDataBoo) {
      //插入历史用户表
      insertHistoryTableIfNull(sparkSession, "history_users", "distinct_id", "tempTabDisId")
      //插入新增用户表
      insertIncreaseTableIfNull(sparkSession,"increase_users","distinct_id","history_users")

    } else {

      //插入历史用户表
      insertHistoryTableNotNull(sparkSession,"history_users","distinct_id","tempTabDisId")
      // 新增用户表的数据从历史用户表中查询
      insertIncreaseTableNotNull(sparkSession,"increase_users","distinct_id","history_users")
    }

    //----------------------------------------------------------------- 以下是插入小店新增

    sparkSession.sql("select shop_id from tempTab group by shop_id having shop_id is not null  ").toDF().createOrReplaceTempView("tempTabShopId")
    // 如果历史表中没有数据，那么其他表中也不会有数据，则本次所查出的 shop_id 全部为新用户
    if (hisDataBoo) {
      //插入历史门店用户表
      insertHistoryTableIfNull(sparkSession, "history_shops", "shop_id", "tempTabShopId")
      //插入新增门店用户表
      insertIncreaseTableIfNull(sparkSession,"increase_shops","shop_id","history_shops")

    } else {

      //插入历史门店用户表
      insertHistoryTableNotNull(sparkSession,"history_shops","shop_id","tempTabShopId")
      // 新增门店用户表的数据从历史门店用户表中查询
      insertIncreaseTableNotNull(sparkSession,"increase_shops","shop_id","history_shops")
    }
    sc.stop()
    sparkSession.stop()

  }

  /**
    * union all 写错了，写成union all变成一列了- -，
    * *
    *sparkSession.sql(
    * """
    * | insert into increase_users
    * |   select
    * |     *
    * |   from
    * |      (
    * |        select
    * |            count(distinct_id)  did
    * |        from history_users
    * |            where insert_time between from_unixtime(unix_timestamp() - 900, 'yyyy-MM-dd HH:mm:ss') and from_unixtime(unix_timestamp() , 'yyyy-MM-dd HH:mm:ss')
    * |      union all
    * |        select
    * |            count(distinct_id) did
    * |        from history_users
    * |            where insert_time between from_unixtime(unix_timestamp(), 'yyyy-MM-dd 00:00:00') and from_unixtime(unix_timestamp(), 'yyyy-MM-dd HH:mm:ss')
    * |      union all
    * |        select
    * |            count(distinct_id) did
    * |        from history_users
    * |           where insert_time between from_unixtime(unix_timestamp(), 'yyyy-MM-01 00:00:00') and from_unixtime(unix_timestamp(), 'yyyy-MM-dd HH:mm:ss')
    * |      union all
    * |        select from_unixtime(unix_timestamp()) did
    * |      ) as tmp
    * """.stripMargin)
    *
    */

}

