package dao;

import com.baomidou.mybatisplus.annotation.TableName;

import java.util.Date;

@TableName("add_user_credit_log")
public class AddCredit {
    private Date addtime;

    public Date getAddtime() {
        return addtime;
    }

    public void setAddtime(Date addtime) {
        this.addtime = addtime;
    }
}
