package mj.data;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

/**
 * 砀山麻游：场结算汇总
 * 每场结束统计积分，生成可复制文本
 *
 * @author zuoge85@gmail.com on 2026/06/04
 */
public class DsMajiangSummary {
    private int chapterMax;  // 总局数
    private int currentChapter;  // 当前局数
    private UserPaiInfo[] userPaiInfos;  // 本局结算信息
    private ArrayList<ChapterEndResult> chapterResults;  // 全场所有局结算

    public DsMajiangSummary() {
        chapterResults = new ArrayList<>();
    }

    public DsMajiangSummary(int chapterMax) {
        this.chapterMax = chapterMax;
        chapterResults = new ArrayList<>();
    }

    /**
     * 添加一局结算结果
     */
    public void addChapterResult(ChapterEndResult result) {
        chapterResults.add(result);
    }

    /**
     * 设置当前局数
     */
    public void setCurrentChapter(int currentChapter) {
        this.currentChapter = currentChapter;
    }

    /**
     * 设置本局结算信息
     */
    public void setUserPaiInfos(UserPaiInfo[] userPaiInfos) {
        this.userPaiInfos = userPaiInfos;
    }

    /**
     * 计算全场累计积分
     */
    public int[] calculateTotalScores() {
        int[] totalScores = new int[4];
        Arrays.fill(totalScores, 0);

        for (ChapterEndResult result : chapterResults) {
            if (result.getUserPaiInfos() != null) {
                for (UserPaiInfo info : result.getUserPaiInfos()) {
                    totalScores[info.getLocationIndex()] += info.getScore();
                }
            }
        }

        return totalScores;
    }

    /**
     * 生成可复制的结算文本
     * 格式：砀山麻游 - 第X局结算
     * 玩家A: +12分 (胡牌3分 x 4)
     * 玩家B: -8分
     * ...
     */
    public String generateSummaryText() {
        StringBuilder sb = new StringBuilder();
        sb.append("砀山麻游 - 第").append(currentChapter).append("局结算\n");
        sb.append("总局数：").append(chapterMax).append("\n\n");

        int[] totalScores = calculateTotalScores();

        // 按分数排序
        Integer[] indices = new Integer[]{0, 1, 2, 3};
        Arrays.sort(indices, (a, b) -> Integer.compare(totalScores[b], totalScores[a]));

        for (int i = 0; i < 4; i++) {
            int idx = indices[i];
            String rank = i == 0 ? "🥇" : i == 1 ? "🥈" : i == 2 ? "🥉" : "4️⃣";
            sb.append(String.format("%s 玩家%d: %s%d分\n",
                    rank,
                    idx + 1,
                    totalScores[idx] >= 0 ? "+" : "",
                    totalScores[idx]));
        }

        sb.append("\n---\n");
        sb.append("复制以上结果分享");

        return sb.toString();
    }

    /**
     * 生成简洁版结算文本（用于复制）
     */
    public String generateCompactText() {
        StringBuilder sb = new StringBuilder();
        sb.append("砀山麻游第").append(currentChapter).append("局: ");

        int[] totalScores = calculateTotalScores();

        for (int i = 0; i < 4; i++) {
            if (i > 0) sb.append(", ");
            sb.append(String.format("玩家%d:%s%d",
                    i + 1,
                    totalScores[i] >= 0 ? "+" : "",
                    totalScores[i]));
        }

        return sb.toString();
    }

    public int getChapterMax() {
        return chapterMax;
    }

    public void setChapterMax(int chapterMax) {
        this.chapterMax = chapterMax;
    }

    public int getCurrentChapter() {
        return currentChapter;
    }

    public ArrayList<ChapterEndResult> getChapterResults() {
        return chapterResults;
    }

    public UserPaiInfo[] getUserPaiInfos() {
        return userPaiInfos;
    }
}
