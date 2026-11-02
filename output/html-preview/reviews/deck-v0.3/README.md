# 《从观看山水到栖居山水》22页HTML视觉初稿

**v0.3-draft；22页全部待审核，确认0／22。未制作正式PPTX，未修改GitHub Pages设置。**

## 打开预览

1. 下载当前分支／PR中的完整目录，打开 [index.html](index.html)。保留相邻CSS、JS、assets、pages和screenshots。
2. 可用上一页／下一页、键盘左右键、页码输入、缩略图总览、单页和全屏。`index.html#P18` 可直达指定页。单页入口如 [P01](pages/P01.html)，各页都有对应文件。
3. 画布16:9、1920×1080，手机整页等比缩放，不重排图文。手机建议横屏；看细节可以打开单页高清PNG再双指放大。部分手机文件管理器不会执行HTML，应使用浏览器或静态HTTP服务。
4. 本地服务：在仓库根目录执行 `python3 -m http.server 8000 --directory output/html-preview`，电脑打开 `http://localhost:8000/`。同一可信局域网手机可访问电脑局域网IP的8000端口（按本机网络策略配置）；云环境不能据此假定公网可达。
5. [standalone.html](standalone.html) 现在是旧入口兼容页，指向本轮22页主入口，**不再声称为自包含单文件**。旧五页版本可从Git基线a137581恢复；P01精修候选仍在 [历史对照](reviews/P01/v0.2/README.md)。

完整当前预览包另存 `../html-preview.zip`；该包只含v0.3当前文件，不含历史reviews目录。历史精修候选请在仓库中查看。

## 截图与审核资料

- `screenshots/P01.png`—`P22.png`：22张1920×1080高清单页，截图仅用于审核，不进入正式PPTX。
- 四张手机友好竖向拼图：[P01—P06](overview-P01-P06.jpg)、[P07—P12](overview-P07-P12.jpg)、[P13—P18](overview-P13-P18.jpg)、[P19—P22](overview-P19-P22.jpg)。
- [页面设计说明](页面设计说明.md)：逐页视觉任务、讲稿锚点、24pt换算与待核事项。
- [图片与文献来源](素材来源.md)：8件真实作品、4个可追溯裁切、电子原文和许可。原始元数据见 `assets/source-records/`；坐标见 `assets/crops.json`。
- `validation.json`：实际浏览器检查；`version-manifest.json`／`page-content.json`：文件／页面指纹；`review-status.json`：22页均待审核、confirmed=false。
- 规范与审核主记录：`../../materials/PPT制作总规范.md`、`../../materials/页面审核记录.md`。原讲稿 `../../materials/身即与透视完整讲稿.docx` 未改写，SHA256仍为5de6342ac72906d530e2e2ea79a432110788b93ab3c7c2567304798ab08803af。

## 检查范围与限制

画布内最低48px，对应拟用13⅓×7.5英寸PPT的24pt；SVG文字按实际变换检查。手机外层控制栏不属于投影内容。中文字体已本地打包，不依赖在线字体。全22页已生成并逐页渲染；检查图片加载、等比显示、文字边界、导航、390×844与844×390视口及单页入口。当前受管Chromium禁止file://（ERR_BLOCKED_BY_ADMINISTRATOR），因此直接本地文件打开未获实测通过；HTTP静态服务预览已通过。实体设备／教室投影仍待实际审核。部分艺术史精确年代、题跋与中译本页码尚待核定，详见来源与设计说明，不提前声称学术最终定稿。

## GitHub Pages预览方案（未执行）

本轮不更改现有Pages设置，也不部署。GitHub仓库的普通文件链接不会渲染HTML。若之后授权发布，先检查现有Pages来源和站点，再选用独立preview目录／部署工作流，将本目录作为静态文件完整发布（无构建、无外部脚本和外部字体），避免覆盖已有站点。未发布前不提供虚假的线上预览URL。

## 后续流程

逐页反馈、逐页修改；只有用户回复“PXX视觉确认”才能冻结该页具体版本。已确认页必须单独留档，禁止共享样式或批量重建意外覆盖。`build_preview.py` 会在存在confirmed=true时拒绝整套重建。正式阶段另获明确授权后，以确认版HTML为依据重建PowerPoint原生文字与图形，艺术作品独立放置，逐页渲染对照；禁止整页截图冒充可编辑PPT。当前完成后暂停。
