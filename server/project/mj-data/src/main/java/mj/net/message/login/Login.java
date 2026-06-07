package mj.net.message.login;

import java.io.IOException;

import com.isnowfox.core.io.Input;
import com.isnowfox.core.io.Output;
import com.isnowfox.core.io.ProtocolException;

import com.isnowfox.core.net.message.AbstractMessage;

/**
 * 登陆信息
 * 
 * <b>生成器生成代码，请勿修改，扩展请继承</b>
 * @author isnowfox消息生成器
 * 砀山麻游：添加密码字段用于密码登录
 */
public class Login extends AbstractMessage{
	public static final int TYPE			 = 7;
	public static final int ID				 = 8;
	
	/**
	 * SMS 短信登录，WEIXIN_CLIENT 微信客户端，TOKEN token登录，PASSWORD 密码登录
	 */
	private String type;
	private String openId;
	private String code;
	/**
	 * 经度
	 */
	private String longitude;
	/**
	 * 纬度
	 */
	private String latitude;
	/**
	 * 砀山麻游：密码字段（用于 PASSWORD 登录类型）
	 */
	private String password;
	
	public Login(){
		
	}
	
	public Login(String type, String openId, String code, String longitude, String latitude) {
		this.type = type;
		this.openId = openId;
		this.code = code;
		this.longitude = longitude;
		this.latitude = latitude;
	}
	
	/**
	 * 砀山麻游：密码登录构造函数
	 */
	public Login(String type, String openId, String password) {
		this.type = type;
		this.openId = openId;
		this.password = password;
	}
	
	@Override
	public void decode(Input in)  throws IOException, ProtocolException {
		type = in.readString();
		openId = in.readString();
		code = in.readString();
		longitude = in.readString();
		latitude = in.readString();
		// 砀山麻游：密码字段（向后兼容：旧客户端可能不发送此字段）
		try {
			password = in.readString();
		} catch (ProtocolException e) {
			password = null;
		}
	}

	@Override
	public void encode(Output out)  throws IOException, ProtocolException {
		out.writeString(getType());
		out.writeString(getOpenId());
		out.writeString(getCode());
		out.writeString(getLongitude());
		out.writeString(getLatitude());
		// 砀山麻游：写入密码字段
		out.writeString(password);
	}

	/**
	 * SMS 短信登录，WEIXIN_CLIENT 微信客户端，TOKEN token登录，PASSWORD 密码登录
	 */
	public String getType() {
		return type;
	}
	
	/**
	 * SMS 短信登录，WEIXIN_CLIENT 微信客户端，TOKEN token登录，PASSWORD 密码登录
	 */
	public void setType(String type) {
		this.type = type;
	}

	public String getOpenId() {
		return openId;
	}
	
	public void setOpenId(String openId) {
		this.openId = openId;
	}

	public String getCode() {
		return code;
	}
	
	public void setCode(String code) {
		this.code = code;
	}

	/**
	 * 经度
	 */
	public String getLongitude() {
		return longitude;
	}
	
	/**
	 * 经度
	 */
	public void setLongitude(String longitude) {
		this.longitude = longitude;
	}

	/**
	 * 纬度
	 */
	public String getLatitude() {
		return latitude;
	}
	
	/**
	 * 纬度
	 */
	public void setLatitude(String latitude) {
		this.latitude = latitude;
	}

	/**
	 * 砀山麻游：密码字段
	 */
	public String getPassword() {
		return password;
	}
	
	/**
	 * 砀山麻游：密码字段
	 */
	public void setPassword(String password) {
		this.password = password;
	}

	
	@Override
	public String toString() {
		return "Login [type=" + type + ",openId=" + openId + ",code=" + code + ",longitude=" + longitude + ",latitude=" + latitude + ",password=" + (password != null ? "***" : "null") + ", ]";
	}
	
	@Override
	public final int getMessageType() {
		return TYPE;
	}

	@Override
	public final int getMessageId() {
		return ID;
	}
}
