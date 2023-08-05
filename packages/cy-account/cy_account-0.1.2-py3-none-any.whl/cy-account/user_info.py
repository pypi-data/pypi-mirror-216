from typing import Optional
from pydantic import BaseModel, ValidationError


class UserInfo(BaseModel):
    """
    user info 的基础模型
    """
    phone: Optional[str] = None
    nick_name: Optional[str] = None
    avatar: Optional[str] = None
    desc: Optional[str] = None
    background: Optional[str] = None
    gender: Optional[int] = 0  # 0不显示  1男 2女
    status: Optional[int] = 1  # 1正常 2冻结
    id: Optional[int] = None

    is_vip: Optional[bool] = False
    vip_end_time: Optional[str] = None
    vip_level: Optional[int] = 1
    points: Optional[int] = 0  # 积分
