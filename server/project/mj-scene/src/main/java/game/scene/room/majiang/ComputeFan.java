package game.scene.room.majiang;

import mj.data.*;
import mj.net.message.game.GameChapterEnd;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Stream;

/**
 * 砀山麻游计分规则：
 * - 胡牌：3分（自摸三家各出3分，点炮放炮者出3分）
 * - 七对胡牌：6分
 * - 明杠（大明杠+碰后杠/小明杠）：1分，三家各出1分
 * - 暗杠：2分，三家各出2分
 * - 赢家不支付杠牌分（赢家除外）
 * - 无马牌、无番数
 */
public class ComputeFan {
    private static final int HU_SCORE = 3;
    private static final int QI_DUI_SCORE = 6;
    private static final int MING_GANG_SCORE = 1;
    private static final int AN_GANG_SCORE = 2;

    private MajiangChapter chapter;
    private ChapterEndResult endResult;

    public ComputeFan(MajiangChapter chapter,
                      int huPaiIndex, int fangPaoIndex, boolean isGangShangHua) {
        this.chapter = chapter;
        endResult = new ChapterEndResult();
        endResult.setHuPai(huPaiIndex != -1);
        endResult.setZhuangIndex(chapter.getZhuangIndex());
        endResult.setHuPaiIndex(huPaiIndex);
        boolean isZiMo = fangPaoIndex == -1;
        endResult.setZiMo(isZiMo);
        endResult.setGangShangHua(isGangShangHua);
        endResult.setFangPaoIndex(fangPaoIndex);
        endResult.setLastPai(chapter.isLastPai());
        endResult.setLeft((ArrayList<Pai>) chapter.getLeftPai().clone());
        endResult.setHuiEr(chapter.getHuiEr());
        endResult.setUserPaiInfos(
                Stream.of(chapter.getUserPlaces()).map(u -> new UserPaiInfo(
                        chapter.getRules().getAllPai(), chapter.getHuiEr(), u,
                        u.getLocationIndex() == huPaiIndex,
                        u.getLocationIndex() == chapter.getZhuangIndex(),
                        isZiMo
                )).toArray(UserPaiInfo[]::new)
        );
    }

    public ChapterEndResult compute() {
        if (endResult.isHuPai()) {
            UserPlace[] userPlaces = chapter.getUserPlaces();
            UserPaiInfo[] userPaiInfos = endResult.getUserPaiInfos();
            calcScore(userPaiInfos);
        }
        return endResult;
    }

    /**
     * 计算最终得分
     * 规则：
     * 1. 胡牌3分（七对6分），自摸三家全出，点炮放炮者出
     * 2. 明杠（大明杠+碰后杠）每家出1分，暗杠每家出2分
     * 3. 赢家不支付杠牌分（赢家除外）
     */
    private void calcScore(UserPaiInfo[] userPaiInfos) {
        int huPaiIndex = endResult.getHuPaiIndex();
        int fangPaoIndex = endResult.getFangPaoIndex();
        boolean isZiMo = endResult.isZiMo();
        int winner = huPaiIndex;

        // 1. 确定胡牌基础分
        UserPaiInfo winnerInfo = userPaiInfos[winner];
        boolean isQiDui = checkQiDui(winnerInfo);
        int huScore = isQiDui ? QI_DUI_SCORE : HU_SCORE;

        // 2. 胡牌得分分配
        if (isZiMo) {
            // 自摸：三家各出3分（或七对6分）
            winnerInfo.setScore(winnerInfo.getScore() + huScore * 3);
            for (int i = 0; i < userPaiInfos.length; i++) {
                if (i != winner) {
                    userPaiInfos[i].setScore(userPaiInfos[i].getScore() - huScore);
                }
            }
        } else {
            // 点炮：放炮者出3分（或七对6分）
            winnerInfo.setScore(winnerInfo.getScore() + huScore);
            userPaiInfos[fangPaoIndex].setScore(userPaiInfos[fangPaoIndex].getScore() - huScore);
        }

        // 3. 杠牌分分配（杠吃三家，赢家除外）
        for (int i = 0; i < userPaiInfos.length; i++) {
            UserPaiInfo info = userPaiInfos[i];
            int gangScore = info.getDaMingGang().size() * MING_GANG_SCORE
                    + info.getXiaoMingGang().size() * MING_GANG_SCORE
                    + info.getAnGang().size() * AN_GANG_SCORE;
            if (gangScore > 0) {
                // 向其他玩家收杠牌分
                for (int j = 0; j < userPaiInfos.length; j++) {
                    if (j != i && j != winner) {
                        // 赢家除外：赢家不支付杠牌分
                        info.setScore(info.getScore() + gangScore);
                        userPaiInfos[j].setScore(userPaiInfos[j].getScore() - gangScore);
                    }
                }
            }
        }
    }

    private boolean checkQiDui(UserPaiInfo info) {
        // 检查是否为七对：手牌 + 碰（如果有碰则不是七对）
        if (!info.getPeng().isEmpty() || !info.getChi().isEmpty()) {
            return false;
        }
        // 七对：14张手牌（胡牌后）= 7个对子
        ArrayList<Pai> shouPai = info.getShouPai();
        if (shouPai.size() != 14) {
            return false;
        }
        // 检查是否都是对子
        return chapter.getUserPlaces()[info.getLocationIndex()].isQiDui();
    }

    public int zaMa() {
        // 砀山麻游没有马牌
        return 0;
    }

    public void computeGuaFengXiaYu() {
        // 杠牌分已在 calcScore 中直接计算，此处不再重复计算
    }
}
