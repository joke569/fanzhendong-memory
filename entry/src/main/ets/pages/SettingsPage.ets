import { router, promptAction } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';
import { MemoryState } from '../model/MemoryModels';
import { MemoryStore } from '../services/MemoryStore';

@Entry
@Component
struct SettingsPage {
  @State reduceMotion: boolean = false;
  @State loaded: boolean = false;
  @State visitedCount: number = 0;
  @State favoriteCount: number = 0;
  private context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;

  aboutToAppear(): void {
    this.load();
  }

  async load(): Promise<void> {
    await MemoryStore.init(this.context);
    const state = await MemoryStore.load();
    this.reduceMotion = state.reduceMotion;
    this.visitedCount = state.visited.length;
    this.favoriteCount = state.favorites.length;
    this.loaded = true;
  }

  async setMotion(value: boolean): Promise<void> {
    this.reduceMotion = value;
    const state = await MemoryStore.load();
    state.reduceMotion = value;
    await MemoryStore.saveState(state);
  }

  async clearData(): Promise<void> {
    await MemoryStore.clearAll();
    promptAction.showToast({ message: '收藏与手记已清空', duration: 1600 });
  }

  @Builder
  SectionTitle(text: string) {
    Text(text)
      .fontSize(10)
      .fontWeight(FontWeight.Bold)
      .fontColor('#E7B768')
      .letterSpacing(1.8)
      .width('100%')
      .margin({ top: 20, bottom: 8 })
  }

  build() {
    Stack({ alignContent: Alignment.TopStart }) {
      Column()
        .width('100%')
        .height('100%')
        .linearGradient({
          direction: GradientDirection.Bottom,
          colors: [
            ['#06070C', 0.0],
            ['#10131C', 0.55],
            ['#06070C', 1.0]
          ]
        })

      Column() {
        Row() {
          Text('←')
            .fontSize(23)
            .fontColor('#F6F2E9')
            .width(36)
            .height(36)
            .textAlign(TextAlign.Center)
            .borderRadius(18)
            .backgroundColor('#26FFFFFF')
            .onClick(() => router.back())
          Text('回忆设置')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#F6F2E9')
            .margin({ left: 12 })
        }
        .width('100%')
        .padding({ left: 16, right: 16, top: 12, bottom: 18 })

        Scroll() {
          Column() {
            this.SectionTitle('EXPERIENCE')

            Row() {
              Column() {
                Text('减少动态效果')
                  .fontSize(14)
                  .fontColor('#F6F2E9')
                Text('关闭自动播放与流动字幕')
                  .fontSize(10)
                  .fontColor('#8CF6F2E9')
                  .margin({ top: 4 })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)

              Toggle({ type: ToggleType.Switch, isOn: this.reduceMotion })
                .selectedColor('#E7B768')
                .switchPointColor('#1A1207')
                .onChange((isOn: boolean) => this.setMotion(isOn))
            }
            .width('100%')
            .padding({ top: 14, bottom: 14 })
            .border({ width: { bottom: 1 }, color: '#14FFFFFF' })

            this.SectionTitle('DATA')

            Row() {
              Column() {
                Text('清空收藏与手记')
                  .fontSize(14)
                  .fontColor('#F6F2E9')
                Text('只清除本地数据，不影响照片')
                  .fontSize(10)
                  .fontColor('#8CF6F2E9')
                  .margin({ top: 4 })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)

              Text('›')
                .fontSize(22)
                .fontColor('#66F6F2E9')
            }
            .width('100%')
            .padding({ top: 14, bottom: 14 })
            .border({ width: { bottom: 1 }, color: '#14FFFFFF' })
            .onClick(() => this.clearData())

            this.SectionTitle('JOURNEY')

            Column() {
              Row() {
                Text('探索进度')
                  .fontSize(12)
                  .fontColor('#D9F6F2E9')
                Blank()
                Text(`${this.visitedCount} / 22`)
                  .fontSize(11)
                  .fontColor('#E7B768')
              }
              .width('100%')

              Progress({ value: this.visitedCount, total: 22, type: ProgressType.Linear })
                .width('100%')
                .height(4)
                .color('#E7B768')
                .backgroundColor('#1FFFFFFF')
                .margin({ top: 8, bottom: 12 })

              Row() {
                Text('收藏')
                  .fontSize(11)
                  .fontColor('#8CF6F2E9')
                Text(`${this.favoriteCount} 段`)
                  .fontSize(11)
                  .fontColor('#E7B768')
                  .margin({ left: 6 })
                Blank()
                Text(this.visitedCount >= 10 ? '已解锁 · 巴黎的金色雨' : '继续探索，解锁隐藏回忆')
                  .fontSize(9)
                  .fontColor(this.visitedCount >= 10 ? '#E7B768' : '#66F6F2E9')
              }
              .width('100%')

              if (this.favoriteCount >= 5) {
                Text('成就 · 三线收藏家：你已经把三条线都留在了手边。')
                  .fontSize(10)
                  .lineHeight(16)
                  .fontColor('#B3F6F2E9')
                  .margin({ top: 10 })
              }
            }
            .width('100%')
            .padding(14)
            .borderRadius(20)
            .backgroundColor('#0FFFFFFF')
            .border({ width: 1, color: '#1FFFFFFF' })

            this.SectionTitle('ABOUT THIS ARCHIVE')

            Column() {
              Text('这是一份独立完成的课程作品，以“生涯 / 球衣 / 球拍”三条线回看樊振东。照片来自公开报道，仅用于课程学习；插画与界面为原创。')
                .fontSize(12)
                .lineHeight(21)
                .fontColor('#B3F6F2E9')
              Text('Photo credits: 新华社 / 人民日报 / 新浪体育 / 萨尔布吕肯俱乐部。版权归原作者所有。')
                .fontSize(9)
                .lineHeight(15)
                .fontColor('#59F6F2E9')
                .margin({ top: 10 })
              Text('Fan Zhendong Memory Archive · 2026 · v1.0')
                .fontSize(9)
                .fontColor('#40F6F2E9')
                .margin({ top: 8 })
            }
            .width('100%')
            .padding(16)
            .borderRadius(22)
            .backgroundColor('#0FFFFFFF')
            .border({ width: 1, color: '#1FFFFFFF' })
          }
          .width('100%')
          .padding({ left: 20, right: 20, bottom: 30 })
        }
        .layoutWeight(1)
        .scrollBar(BarState.Off)
      }
      .width('100%')
      .height('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#06070C')
  }
}
