package game.scene.room.majiang.rules;

import game.scene.room.majiang.PaiPool;
import mj.data.*;
import org.apache.commons.lang.math.RandomUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * 砀山麻游规则
 * - 花牌只有中发白（各4张，共12张）
 * - 不能吃牌，只能碰、杠、胡
 * - 碰牌后可再杠
 * - 明杠1分，暗杠2分，胡牌3分
 * - 七对翻倍
 * - 可截胡，可胡碰后杠
 *
 * @author zuoge85@gmail.com on 2026/06/04
 */
class DsMajiangRules extends Rules {
    // 120张牌：筒36 + 条36 + 万36 + 花牌12 = 120
    private static final ArrayList<Pai> ALL_PAI_LIST = createAllList();

    public static final Map<JiaFanType, FanInfo> jiaFanMap = initJiaFanMap();
    public static final Map<BaseFanType, FanInfo> baseFanMap = initBaseFanMap();

    private static Map<JiaFanType, FanInfo> initJiaFanMap() {
        Map<JiaFanType, FanInfo> map = new HashMap<>();
        // 砀山麻游加番
        map.put(JiaFanType.ZHUANG_HU, new FanInfo("庄胡", 1));
        map.put(JiaFanType.QI_DUI, new FanInfo("七对", 0));  // 七对翻倍，基础番数在 baseFanMap 中
        return map;
    }

    private static Map<BaseFanType, FanInfo> initBaseFanMap() {
        Map<BaseFanType, FanInfo> map = new HashMap<>(BaseFanType.baseFanMap);
        // 砀山麻游基础番数
        // 胡牌3分，明杠1分，暗杠2分
        map.replace(BaseFanType.HUI_ER_GANG, new FanInfo("自摸", 3));
        map.replace(BaseFanType.ZI_MO, new FanInfo("自摸", 3));
        map.replace(BaseFanType.JI_HU, new FanInfo("", 3));  // 胡牌基础3分
        map.replace(BaseFanType.DUI_DUI_HU, new FanInfo("对对胡", 3));
        map.replace(BaseFanType.QI_DUI, new FanInfo("七对子", 6));  // 七对翻倍（3*2=6）
        map.replace(BaseFanType.TIAN_HU, new FanInfo("天胡", 10));
        map.replace(BaseFanType.DI_HU, new FanInfo("地胡", 10));
        // 明杠1分，暗杠2分（在 ComputeFan 中计算）
        return map;
    }

    private static ArrayList<Pai> createAllList() {
        ArrayList<Pai> list = new ArrayList<>();

        // 筒子 1-9 各1张（PaiPool.start() 会×4）
        for (int paiIndex = Pai.TONG_1.getIndex(); paiIndex <= Pai.TONG_9.getIndex(); paiIndex++) {
            list.add(Pai.fromIndex(paiIndex));
        }

        // 条子 1-9 各1张
        for (int paiIndex = Pai.TIAO_1.getIndex(); paiIndex <= Pai.TIAO_9.getIndex(); paiIndex++) {
            list.add(Pai.fromIndex(paiIndex));
        }

        // 万子 1-9 各1张
        for (int paiIndex = Pai.WAN_1.getIndex(); paiIndex <= Pai.WAN_9.getIndex(); paiIndex++) {
            list.add(Pai.fromIndex(paiIndex));
        }

        // 花牌（中发白）各1张（PaiPool.start() 会×4）
        list.add(Pai.HUAPAI_ZHONG);
        list.add(Pai.HUAPAI_FA);
        list.add(Pai.HUAPAI_BEI);

        // 总计：9 + 9 + 9 + 3 = 30张，PaiPool ×4 = 120张
        return list;
    }

    private Pai[] huiErs;

    DsMajiangRules(Config config) {
        super(config);
    }

    @Override
    public boolean rest() {
        // 砀山麻游没有鬼牌（万用牌）
        huiErs = null;
        return false;
    }

    @Override
    public ArrayList<Pai> getAllPai() {
        return ALL_PAI_LIST;
    }

    @Override
    public Pai[] getHuiEr(PaiPool paiPool) {
        // 砀山麻游没有鬼牌
        return null;
    }

    @Override
    public boolean isChi() {
        // 砀山麻游不能吃牌
        return false;
    }

    @Override
    public boolean isFangPao() {
        // 砀山麻游可以放炮
        return true;
    }

    @Override
    public boolean isZaMa() {
        // 砀山麻游没有码
        return false;
    }

    @Override
    public int getZaMa() {
        return 0;
    }

    @Override
    public Map<JiaFanType, FanInfo> getJiaFanMap() {
        return jiaFanMap;
    }

    @Override
    public Map<BaseFanType, FanInfo> getBaseFanMap() {
        return baseFanMap;
    }

    @Override
    public boolean isHuiGang() {
        // 砀山麻游没有鬼杠
        return false;
    }

    @Override
    public int getBaoliuLength() {
        // 砀山麻游留12张牌（3轮杠牌）
        return 12;
    }
}
