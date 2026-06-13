/**Created by the LayaAirIDE,do not modify.*/
package ui.test {
	import laya.ui.*;
	import laya.display.*;

	public class LoadingUI extends View {
		public var bg:Image;
		public var progressBar:ProgressBar;
		public var progressBarLabel:Label;

		public static var uiView:Object ={"type":"View","props":{"width":1920,"height":1080},"child":[{"type":"Image","props":{"y":0,"x":0,"width":1920,"var":"bg","skin":"ui/loading/bg.jpg","height":1080,"sizeGrid":"0,0,0,0"}},{"type":"ProgressBar","props":{"y":972,"x":830,"width":260,"var":"progressBar","skin":"ui/loading/progress.png","sizeGrid":"11,7,12,7","height":24}},{"type":"Label","props":{"y":975,"x":830,"width":260,"var":"progressBarLabel","text":"加载中 100%","height":38,"fontSize":24,"color":"#ffffff","align":"center"}}]};
		override protected function createChildren():void {
			super.createChildren();
			createView(uiView);
		}
	}
}