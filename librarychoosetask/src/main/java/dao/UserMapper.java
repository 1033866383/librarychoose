package dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface UserMapper extends BaseMapper<User> {

    @Select("select *, role_id as roleId from users")
    public List<User> all();

    @Update("update users set info = #{info} where id = #{id}")
    public int updateById(User u);

}
