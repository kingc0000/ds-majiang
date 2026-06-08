package mj.data;

import mj.net.message.game.GameChapterEnd;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

/**
 * 牌局结束结果集
 *
 * @author zuoge85@gmail.com on 2016/11/4.
 */
public class ChapterEndResult {
    private boolean isHuPai;
    private int huPaiIndex;
    private int zhuangIndex;
    private UserPaiInfo[] userPaiInfos;
    private ArrayList<Pai> left;//剩下的
    private boolean isZiMo;
    private Pai[] huiEr;
    private boolean isGangShangHua;
    private boolean isLastPai;
    private int fangPaoIndex;

    public ChapterEndResult() {

    }

    /**
     * 砀山麻游新版：分数已在 ComputeFan.calcScore 中直接计算，
     * 此处仅同步 fan 字段供客户端显示
     */
    public void excuteScore() {
        for (int i = 0; i < userPaiInfos.length; i++) {
            userPaiInfos[i].setFan(userPaiInfos[i].getScore());
        }
    }

    public GameChapterEnd toMessage() {
        GameChapterEnd m = new GameChapterEnd();
        m.setFangPaoIndex(fangPaoIndex);
        m.setHuPaiIndex(huPaiIndex);
        m.setZaMaFan(0);
        m.setZaMaPai(new int[0]);
        m.setZaMaType(0);

        m.setFanResults(Arrays.stream(userPaiInfos)
                .map(UserPaiInfo::toMessage)
                .collect(Collectors.toCollection(ArrayList::new))
        );
        return m;
    }

    public int getFanNums() {
        return userPaiInfos[huPaiIndex].getFanNums();
    }

    public FanResult getMaxFanResult() {
        return userPaiInfos[huPaiIndex].getMaxFanResult();
    }

    public boolean isHuPai() {
        return isHuPai;
    }

    public void setHuPai(boolean huPai) {
        isHuPai = huPai;
    }

    public int getHuPaiIndex() {
        return huPaiIndex;
    }

    public void setHuPaiIndex(int huPaiIndex) {
        this.huPaiIndex = huPaiIndex;
    }

    public int getZhuangIndex() {
        return zhuangIndex;
    }

    public void setZhuangIndex(int zhuangIndex) {
        this.zhuangIndex = zhuangIndex;
    }

    public UserPaiInfo[] getUserPaiInfos() {
        return userPaiInfos;
    }

    public void setUserPaiInfos(UserPaiInfo[] userPaiInfos) {
        this.userPaiInfos = userPaiInfos;
    }

    public ArrayList<Pai> getLeft() {
        return left;
    }

    public void setLeft(ArrayList<Pai> left) {
        this.left = left;
    }

    public boolean isGangShangHua() {
        return isGangShangHua;
    }

    public Pai[] getHuiEr() {
        return huiEr;
    }

    public void setHuiEr(Pai[] huiEr) {
        this.huiEr = huiEr;
    }

    public boolean isZiMo() {
        return isZiMo;
    }

    public boolean isLastPai() {
        return isLastPai;
    }

    public int getFangPaoIndex() {
        return fangPaoIndex;
    }

    public void setZiMo(boolean ziMo) {
        isZiMo = ziMo;
    }

    public void setGangShangHua(boolean gangShangHua) {
        isGangShangHua = gangShangHua;
    }

    public void setLastPai(boolean lastPai) {
        isLastPai = lastPai;
    }

    public void setFangPaoIndex(int fangPaoIndex) {
        this.fangPaoIndex = fangPaoIndex;
    }

    @Override
    public String toString() {
        return "ChapterEndResult{" +
                "isHuPai=" + isHuPai +
                ", huPaiIndex=" + huPaiIndex +
                ", zhuangIndex=" + zhuangIndex +
                ", userPaiInfos=" + Arrays.toString(userPaiInfos) +
                ", left=" + left +
                ", isZiMo=" + isZiMo +
                ", huiEr=" + Arrays.toString(huiEr) +
                ", isGangShangHua=" + isGangShangHua +
                ", isLastPai=" + isLastPai +
                ", fangPaoIndex=" + fangPaoIndex +
                '}';
    }
}
