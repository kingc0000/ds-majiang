package majiang.client.db;

import majiang.client.utils.JsonUtils;
import org.iq80.leveldb.DB;
import org.iq80.leveldb.Options;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import org.fusesource.leveldbjni.JniDBFactory;

/**
 * @author zuoge85@gmail.com on 2016/12/8.
 */
@Component
public class DbManager {

    public static final String CHARSET_NAME = "utf8";
    private DB db;
    private volatile boolean isClose = true;
    private boolean levelDbAvailable = true;

    @PostConstruct
    public void init() {
        try {
            Options options = new Options();
            options.createIfMissing(true);
            File path = new File("db/weixinDb.db");
            if (!path.exists()) {
                path.mkdirs();
            }
            db = new JniDBFactory().open(path, options);
            isClose = false;
            System.out.println("LevelDB 初始化成功");
        } catch (UnsatisfiedLinkError e) {
            // LevelDB JNI 库不可用（架构不兼容），记录警告但不阻止启动
            System.err.println("警告：LevelDB JNI 库不可用，数据库功能将不可用。原因: " + e.getMessage());
            levelDbAvailable = false;
        } catch (IOException e) {
            System.err.println("警告：LevelDB 初始化失败。原因: " + e.getMessage());
            levelDbAvailable = false;
        }

        if (levelDbAvailable) {
            Runtime.getRuntime().addShutdownHook(new Thread() {
                @Override
                public void run() {
                    try {
                        close();
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                }
            });
        }
    }

    public <T> T get(Class<T> cls, String key) {
        if (!levelDbAvailable) return null;
        try {
            byte[] keyBytes = (cls.getName() + "_" + key).getBytes(CHARSET_NAME);
            byte[] value = db.get(keyBytes);

            if (value == null) {
                return null;
            }
            return JsonUtils.deserialize(new String(value, CHARSET_NAME), cls);
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }

    public <T> void save(String key, T t) {
        if (!levelDbAvailable) return;
        Class<?> cls = t.getClass();
        try {
            byte[] keyBytes = (cls.getName() + "_" + key).getBytes(CHARSET_NAME);
            db.put(
                    keyBytes,
                    JsonUtils.serialize(t).getBytes(CHARSET_NAME)
            );
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }


    public byte[] get(String type, String key) {
        if (!levelDbAvailable) return null;
        try {
            byte[] keyBytes = (type + "_" + key).getBytes(CHARSET_NAME);
            return db.get(keyBytes);
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }

    public void save(String type, String key, byte[] data) {
        if (!levelDbAvailable) return;
        try {
            byte[] keyBytes = (type + "_" + key).getBytes(CHARSET_NAME);
            db.put(
                    keyBytes,
                    data
            );
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }


    @PreDestroy
    public void close() throws IOException {
        if (!isClose && levelDbAvailable) {
            synchronized (this) {
                if (!isClose) {
                    db.close();
                }
            }
        }
    }
}
