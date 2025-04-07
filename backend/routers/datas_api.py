from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Dict, Any
from datetime import datetime
# pip install python-jose[cryptography] python-multipart
router = APIRouter()

# 课程表数据
SCHEDULE_DATA = {
    "202401": {
        "monday": ["早读", "语文", "数学", "英语", "物理", "化学", "生物", "历史", "地理", "晚自习", "晚自习", "晚自习", "晚自习"],
        "tuesday": ["早读", "数学", "语文", "英语", "化学", "物理", "政治", "地理", "历史", "晚自习", "晚自习", "晚自习", "晚自习"],
        "wednesday": ["早读", "英语", "物理", "数学", "语文", "生物", "历史", "化学", "地理", "晚自习", "晚自习", "晚自习", "晚自习"],
        "thursday": ["早读", "物理", "化学", "语文", "数学", "英语", "地理", "生物", "政治", "晚自习", "晚自习", "晚自习", "晚自习"],
        "friday": ["早读", "化学", "物理", "数学", "语文", "英语", "政治", "历史", "生物", "晚自习", "晚自习", "晚自习", "晚自习"]
    },
    "202402": {
        "monday": ["早读", "数学", "语文", "英语", "物理", "化学", "生物", "历史", "地理张", "晚自习", "晚自习", "晚自习", "晚自习"],
        "tuesday": ["早读", "语文", "数学", "英语", "化学", "物理", "政治", "地理", "历史", "晚自习", "晚自习", "晚自习", "晚自习"],
        "wednesday": ["早读", "英语", "物理", "数学", "语文", "生物", "历史", "化学", "地理", "晚自习", "晚自习", "晚自习", "晚自习"],
        "thursday": ["早读", "物理", "化学", "语文", "数学", "英语", "地理张", "生物", "政治", "晚自习", "晚自习", "地理张", "晚自习"],
        "friday": ["早读", "化学", "物理", "数学", "语文", "英语", "政治", "历史", "生物", "晚自习", "晚自习", "晚自习", "晚自习"]
    }
}

# 教师数据
TEACHERS_DATA = {
    "王老师": ["语文", "早读", "生物", "政治"],
    "李老师": ["数学", "早读", "历史"],
    "张老师": ["英语", "地理张"],
    "刘老师": ["物理", "早读"],
    "赵老师": ["化学", "早读"]
}

# 作息时间
PERIODS = {
    "早读": "07:30-08:00",
    "第一节": "08:10-08:55",
    "第二节": "09:05-09:50",
    "第三节": "10:10-10:55",
    "第四节": "11:05-11:50",
    "第五节": "13:00-14:45",
    "第六节": "14:55-15:40",
    "第七节": "15:50-16:35",
    "第八节": "16:45-17:30",
    "晚1": "18:30-19:30",
    "晚2": "19:40-20:00",
    "晚3": "20:30-21:00",
    "晚4": "21:00-21:30",
}

# 作业数据
HOMEWORK_DATA = {
    "202401": [
        {
            "id": 1,
            "subject": "语文",
            "teacher": "王老师",
            "content": "完成《论语》阅读笔记，要求不少于1000字,完成《论语》阅读笔记，要求不少于1000字完成《论语》阅读笔记，要求不少于1000字完成《论语》阅读笔记，要求不少于1000字完成《论语》阅读笔记，要求不少于1000字",
            "deadline": "2024-12-13",
            "assigned_date": "2024-12-07",
            "status": "pending",
            "duration": 60,  # 预计完成时间（分钟）
            "type": "daily"  # 日常作业
        },
        {
            "id": 2,
            "subject": "数学",
            "teacher": "李老师",
            "content": "完成教材P123-125的练习题",
            "deadline": "2024-12-14",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 45,
            "type": "daily"
        },
        {
            "id": 3,
            "subject": "英语",
            "teacher": "张老师",
            "content": "完成一篇英语作文：My Dream Job",
            "deadline": "2024-12-11",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 30,
            "type": "daily"
        },
        {
            "id": 4,
            "subject": "物理",
            "teacher": "刘老师",
            "content": "完成本周实验报告",
            "deadline": "2024-12-15",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 90,
            "type": "weekly"
        },
        {
            "id": 5,
            "subject": "化学",
            "teacher": "赵老师",
            "content": "完成元素周期表背诵和测试",
            "deadline": "2024-12-16",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 120,
            "type": "weekly"
        },
        {
            "id": 6,
            "subject": "语文",
            "teacher": "王老师",
            "content": "完成寒假读书计划",
            "deadline": "2024-12-15",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 180,
            "type": "weekly"
        }
    ],
    "202402": [
        {
            "id": 1,
            "subject": "数学",
            "teacher": "李老师",
            "content": "完成教材P123-125的练习题",
            "deadline": "2024-12-10",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 45,
            "type": "daily"
        },
        {
            "id": 2,
            "subject": "英语",
            "teacher": "张老师",
            "content": "完成一篇英语作文：My Dream Job",
            "deadline": "2024-12-11",
            "assigned_date": "2024-12-09",  
            "status": "pending",
            "duration": 30,
            "type": "daily"
        },
        {
            "id": 3,
            "subject": "物理",
            "teacher": "刘老师",
            "content": "完成本周实验报告",
            "deadline": "2024-12-15",
            "assigned_date": "2024-12-09",
            "status": "pending",
            "duration": 90,
            "type": "weekly"
        }
    ]
} 

# 模拟不同班级的公告数据
ANNOUNCEMENTS_DATA = {
    "202401": [
        {
            "id": 1,
            "title": "期中考试安排",
            "content": "下周一开始期中考试，请同学们做好准备。考试科目包括语文、数学、英语、物理、化学，请同学们合理安排复习时间。",
            "date": "2024-12-15"
        },
        {
            "id": 2,
            "title": "班级文艺汇演",
            "content": "本周五下午将举行班级文艺汇演，请报名参演的同学准时到达礼堂进行彩排。观众可以在下午2点入场。",
            "date": "2024-12-10"
        },
        {
            "id": 3,
            "title": "心理健康讲座",
            "content": "本周三下午第三节课将举行心理健康讲座，主题是'如何平衡学习与生活'，请同学们按时参加。",
            "date": "2024-12-13"
        }
    ],
    "202402": [
        {
            "id": 1,
            "title": "运动会参赛通知",
            "content": "下周二是校运动会，我班参加4x100米接力、跳远、铅球等项目的同学请做好准备。",
            "date": "2024-12-12"
        },
        {
            "id": 2,
            "title": "班级大扫除",
            "content": "本周五下午最后一节课进行班级大扫除，请同学们做好准备，带好清洁工具。",
            "date": "2024-12-10"
        }
    ]
}

# 模拟不同班级的班主任寄语数据
TEACHER_MESSAGES = {
    "202401": {
        "content": "亲爱的同学们，在新的学期里，希望大家能够以饱满的热情投入学习。记住，成功不是偶然的，而是来自于每一天的积累和努力。让我们携手共创一个积极向上、团结互助的班级氛围！",
        "teacher": "张明",
        "date": "2024-12-08"
    },
    "202402": {
        "content": "同学们好！新的学期意味着新的机遇和挑战。希望大家能够互帮互助，共同进步。记住：没有什么困难是克服不了的，关键是要有坚持的信念和努力的决心。",
        "teacher": "李华",
        "date": "2024-12-08"
    }
}

# 模拟不同班级的基本信息数据
CLASS_INFO = {
    "202401": {
        "className": "高三一班",
        "classTeacher": "张明",
        "studentCount": 45,
        "established": "2022-09-01",
        "motto": "勤奋学习，追求卓越",
        "location": "教学楼A301",
        "monitorName": "李小明",
        "leagueSecretaryName": "王丽"
    },
    "202402": {
        "className": "高三二班",
        "classTeacher": "李华",
        "studentCount": 48,
        "established": "2022-09-01",
        "motto": "团结协作，共创佳绩",
        "location": "教学楼A302",
        "monitorName": "张伟",
        "leagueSecretaryName": "陈琳"
    }
}

# 添加学生名单模拟数据
MOCK_STUDENTS = {
    "202401": [
        "张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十",
        "钱一", "孙二", "周三", "吴四", "郑五", "王六", "赵七", "钱八",
        "孙九", "周十", "吴十一", "郑十二"
    ],
    "202402": [
        "刘一", "陈二", "张三", "李四", "王五", "赵六", "孙七", "周八",
        "吴九", "郑十", "钱十一", "孙十二", "周十三", "吴十四", "郑十五"
    ],
    "202403": [
        "王一", "李二", "张三", "刘四", "陈五", "杨六", "赵七", "钱八",
        "孙九", "周十", "吴十一", "郑十二", "王十三", "李十四", "张十五",
        "刘十六", "陈十七", "杨十八"
    ]
}

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel

# JWT配置
SECRET_KEY = "your-secret-key"  # 在实际应用中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 用户数据
USERS_DATA = {
    "admin": {
        "username": "admin",
        "hashed_password": "123456",  # 实际应用中应该使用哈希密码
        "role": "admin"
    },
    "teacher": {
        "username": "teacher",
        "hashed_password": "123456",
        "role": "teacher"
    }
}

# 认证相关模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    role: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 认证相关函数
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def get_user(username: str):
    if username in USERS_DATA:
        user_dict = USERS_DATA[username]
        return User(username=user_dict["username"], role=user_dict["role"])
    return None

def authenticate_user(username: str, password: str):
    if username not in USERS_DATA:
        return False
    user = USERS_DATA[username]
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# 登录接口
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 获取所有班级代码
@router.get("/class-codes")
async def get_class_codes():
    """获取所有可用的班级代码"""
    return {"class_codes": list(SCHEDULE_DATA.keys())}

@router.get("/schedule/{class_code}")
async def get_class_schedule(class_code: str):
    """获取指定班级的课程表"""
    if class_code not in SCHEDULE_DATA:
        raise HTTPException(status_code=404, detail="未找到该班级的课程表")
    return {"schedule": SCHEDULE_DATA[class_code]}

@router.get("/homework/{class_code}")
async def get_homework(class_code: str):
    """获取作业列表，按类型分类并过滤过期作业"""
    if class_code not in HOMEWORK_DATA:
        return {"daily": [], "weekly": []}

    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 按类型分类作业
    homework_by_type = {"daily": [], "weekly": []}
    teacher_latest = {}  # 用于记录每个老师最新的作业
    
    # 首先按时间排序
    sorted_homework = sorted(
        HOMEWORK_DATA[class_code],
        key=lambda x: (x["assigned_date"], x["deadline"]),
        reverse=True
    )
    
    # 过滤和分类作业
    for hw in sorted_homework:
        # 跳过已过期的作业
        if hw["deadline"] < current_date:
            continue
            
        # 为每个老师的每种类型只保留最新的作业
        teacher_key = f"{hw['teacher']}_{hw['type']}"
        if teacher_key not in teacher_latest:
            teacher_latest[teacher_key] = hw
            homework_by_type[hw["type"]].append(hw)
    
    return homework_by_type

@router.get("/announcements/{class_code}")
async def get_class_announcements(class_code: str):
    """获取指定班级的公告"""
    if class_code not in ANNOUNCEMENTS_DATA:
        return {"announcements": []}
    return {"announcements": ANNOUNCEMENTS_DATA[class_code]}

@router.get("/messages/{class_code}")
async def get_teacher_messages(class_code: str):
    """获取指定班级的老师留言"""
    if class_code not in TEACHER_MESSAGES:
        return {"messages": []}
    return {"messages": [TEACHER_MESSAGES[class_code]]}

@router.get("/class-info/{class_code}")
async def get_class_info(class_code: str):
    """获取指定班级的基本信息"""
    if class_code not in CLASS_INFO:
        raise HTTPException(status_code=404, detail="未找到该班级的基本信息")
    return {"class_info": CLASS_INFO[class_code]}

@router.get("/students/{class_code}")
async def get_students(class_code: str):
    """获取指定班级的学生名单"""
    students = MOCK_STUDENTS.get(class_code, [])
    return {"students": students}

@router.get("/periods")
async def get_periods():
    """获取课程时间安排"""
    return {"periods": PERIODS}

@router.get("/current-classes", dependencies=[Depends(get_current_user)])
async def get_current_classes():
    """获取当前所有班级正在上的课程"""
    current_time = datetime.now().strftime("%H:%M")
    current_classes = {}
    
    for class_code, schedule in SCHEDULE_DATA.items():
        current_period = None
        
        # 检查当前时间属于哪个课节
        for period, time_range in PERIODS.items():
            start_time, end_time = time_range.split("-")
            if start_time <= current_time <= end_time:
                current_period = period
                break
        
        if current_period is not None:
            # 获取当前是星期几
            weekday = datetime.now().weekday()
            weekday_map = {
                0: "monday",
                1: "tuesday",
                2: "wednesday",
                3: "thursday",
                4: "friday"
            }
            
            if weekday in weekday_map:  # 周一到周五
                day_name = weekday_map[weekday]
                day_schedule = schedule.get(day_name, [])
                period_index = list(PERIODS.keys()).index(current_period)
                
                if 0 <= period_index < len(day_schedule):
                    subject = day_schedule[period_index]
                    # 根据科目查找对应的教师
                    teacher = None
                    for t, subjects in TEACHERS_DATA.items():
                        if subject in subjects:
                            teacher = t
                            break
                    
                    current_classes[class_code] = {
                        "subject": subject,
                        "teacher": teacher or "未知教师",
                        "period": current_period
                    }
    
    return {"current_classes": current_classes}

@router.get("/teacher-schedule/{teacher_name}", dependencies=[Depends(get_current_user)])
async def get_teacher_schedule(teacher_name: str):
    """获取指定教师的课表"""
    if teacher_name not in TEACHERS_DATA:
        raise HTTPException(status_code=404, detail="教师不存在")
    
    teacher_subjects = TEACHERS_DATA[teacher_name]
    teacher_schedule = {str(i): {} for i in range(1, 6)}  # 周一到周五
    weekday_map = {
        "monday": "1",
        "tuesday": "2",
        "wednesday": "3",
        "thursday": "4",
        "friday": "5"
    }
    
    for class_code, schedule in SCHEDULE_DATA.items():
        for day_name, day_schedule in schedule.items():
            day_number = weekday_map.get(day_name)
            if day_number:
                for period_index, subject in enumerate(day_schedule):
                    if subject in teacher_subjects:
                        period = list(PERIODS.keys())[period_index]
                        if period not in teacher_schedule[day_number]:
                            teacher_schedule[day_number][period] = []
                        teacher_schedule[day_number][period].append({
                            "class_code": class_code,
                            "subject": subject
                        })
    
    return {"schedule": teacher_schedule}

@router.get("/teachers", dependencies=[Depends(get_current_user)])
async def get_teachers():
    """获取所有教师列表"""
    return {"teachers": list(TEACHERS_DATA.keys())}

# 错误处理示例
@router.get("/announcement-detail/{class_code}/{announcement_id}")
async def get_announcement_detail(class_code: str, announcement_id: int):
    """获取指定班级的具体公告"""
    # 先检查班级是否存在
    if class_code not in ANNOUNCEMENTS_DATA:
        raise HTTPException(status_code=404, detail="未找到该班级的公告")
    
    # 在该班级的公告中查找指定ID的公告
    announcement = next(
        (a for a in ANNOUNCEMENTS_DATA[class_code] if a["id"] == announcement_id), None
    )
    
    if not announcement:
        raise HTTPException(status_code=404, detail="公告未找到")
    
    return announcement
