import pandas as pd
import time
import eventlet  # 导入eventlet这个模块

hugegraph_conn = PHugeGraph("10.22.32.24", "8080",
                            user="admin", pwd="admin", graph="exercise")


# hugegraph_conn = PyHugeGraph(kv_dict['graph_host'], kv_dict['graph_port'],
#                      user=kv_dict['graph_user'], pwd=kv_dict['graph_pwd'], graph="exercise")
def get_date_from_hugegraph(student_id, chapter_id_list):
    chapter_ids = '\',\''.join(chapter_id_list)
    is_read = False
    df = pd.DataFrame()
    eventlet.monkey_patch()
    # 超过 300ms 视为查询 HugeGraph 失败，返回 false 继续查 MySQL（正常则跳过 MySQL）
    with eventlet.Timeout(0.300, False):
        try:
            start_time = time.time()
            gremlin = """ 
                    g.V('%s')
                     .outE('record').has('chapter_id', within('%s'))
                     .valueMap('chapter_id', 'question_uid', 'answer_status', 'create_time')
                     .limit(500)
                """ % (student_id, chapter_ids)
            # .order().by('create_time',desc)
            res = hugegraph_conn.gremlin().exec(gremlin.strip())
            df = pd.DataFrame(res.get("data")).rename(columns={"question_uid": "uuid"})
            if df.size != 0:
                df.insert(0, 'student_id', student_id)
            is_read = True
        except Exception as e:
            print('student_id: %s; chapter_id: %s' % (student_id, chapter_ids), e)
    print('Read from HugeGraph: %s; %d rows; %.2f ms' %
          (is_read, len(df), (time.time() - start_time) * 1000))
    return is_read, df


if __name__ == '__main__':
    student_id = "gqhyvpzpvvitjrusrvjtzjzq1851z191"
    chapter_id = ["ca47a59379af11e8a10c1c1b0d1c49aa", "c32e574779af11e8a10c1c1b0d1c49aa",
                  "eef1b0af9fa211e88d241c1b0d1c49aa"]
    is_read, df = get_date_from_hugegraph(student_id, chapter_id)
