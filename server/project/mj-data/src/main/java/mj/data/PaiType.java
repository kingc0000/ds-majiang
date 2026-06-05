package mj.data;

/**
 * @author zuoge85@gmail.com on 16/10/17.
 */
public enum PaiType {
    //    筒、条、万
    TONG("筒", false),
    TIAO("条", false),
    WAN("万", false),
    FENG("风", true),
    SANYUAN("三元", true),
    HUAPAI("花牌", true);  // 砀山麻游：中发白作为花牌

    private final String name;
    private final boolean isZhi;

    PaiType(String name, boolean isZhi) {
        this.name = name;
        this.isZhi = isZhi;
    }

    public String getName() {
        return name;
    }

    public boolean isZhi() {
        return isZhi;
    }
}
