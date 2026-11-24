import { router, promptAction } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';
import { MEMORIES } from '../data/MemoryData';
import { MemoryItem, MemoryLine, MemoryState, DetailParams, lineEn } from '../model/MemoryModels';
import { MemoryStore } from '../services/MemoryStore';

@Entry
@Component
struct DetailPage {
  @State item: MemoryItem = MEMORIES[0];
  @State note: string = '';
  @State isFav: boolean = false;
  @State status: string = '自动保存';
  @State noteLoaded: boolean = false;
  private context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;

  aboutToAppear(): void {
    this.load();
  }

  async load(): Promise<void> {
    await MemoryStore.init(this.context);
    const params = router.getParams() as DetailParams;
    if (params && params.id) {
      const found = MEMORIES.find((item: MemoryItem) => item.id === params.id);
      if (found) {
        this.item = found;
      }
    }
    const state = await MemoryStore.load();
    this.isFav = state.favorites.indexOf(this.item.id) >= 0;
    this.note = await MemoryStore.getNote(this.item.id);
    this.status = this.note.length > 0 ? '已保存' : '自动保存';
    this.noteLoaded = true;
  }

  async toggleFav(): Promise<void> {
    const state = await MemoryStore.load();
    const index = state.favorites.indexOf(this.item.id);
    if (index >= 0) {
      state.favorites.splice(index, 1);
      this.isFav = false;
      promptAction.showToast({ message: '已取消收藏', duration: 1400 });
    } else {
      state.favorites.push(this.item.id);
      this.isFav = true;
      promptAction.showToast({ message: '已收藏这段回忆', duration: 1400 });
    }
    await MemoryStore.saveState(state);
  }

  async saveNote(): Promise<void> {
    await MemoryStore.saveNote(this.item.id, this.note);
    this.status = '已保存';
    promptAction.showToast({ message: '手记已保存', duration: 1400 });
  }

  private step(delta: number): void {
    const index = MEMORIES.findIndex((item: MemoryItem) => item.id === this.item.id);
    if (index < 0) {
      return;
    }
    const next = (index + delta + MEMORIES.length) % MEMORIES.length;
    router.replaceUrl({
      url: 'pages/DetailPage',
      params: { id: MEMORIES[next].id }
    });
  }

  @Builder
  Tag(text: string) {
    Text(text)
      .fontSize(10)
      .fontColor('#B3F6F2E9')
      .padding({ left: 10, right: 10, top: 5, bottom: 5 })
      .borderRadius(13)
      .backgroundColor('#14FFFFFF')
      .border({ width: 1, color: '#1FFFFFFF' })
      .margin({ right: 7, bottom: 7 })
  }

  @Builder
  MetaRow(label: string, value: string) {
    Row() {
      Text(label)
        .fontSize(11)
        .fontColor('#8CF6F2E9')
      Blank()
      Text(value)
        .fontSize(11)
        .fontColor('#D9F6F2E9')
        .textAlign(TextAlign.End)
        .maxLines(2)
    }
    .width('100%')
    .padding({ top: 10, bottom: 10 })
    .border({ width: { bottom: 1 }, color: '#14FFFFFF' })
  }

  build() {
    Stack({ alignContent: Alignment.TopStart }) {
      Image(this.item.image)
        .width('100%')
        .height('100%')
        .objectFit(ImageFit.Cover)
        .blur(55)
        .opacity(0.22)

      Column()
        .width('100%')
        .height('100%')
        .linearGradient({
          direction: GradientDirection.Bottom,
          colors: [
            ['#CC06070C', 0.0],
            ['#990B0E16', 0.45],
            ['#F206070C', 1.0]
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
            .backgroundColor('#33FFFFFF')
            .onClick(() => router.back())

          Text(lineEn(this.item.line))
            .fontSize(9)
            .fontWeight(FontWeight.Bold)
            .fontColor(this.item.accent)
            .letterSpacing(1.8)
            .margin({ left: 10 })

          Blank()

          Text(this.isFav ? '♥ 已收藏' : '♡ 收藏')
            .fontSize(10)
            .fontColor(this.isFav ? '#E7B768' : '#D9F6F2E9')
            .padding({ left: 11, right: 11, top: 7, bottom: 7 })
            .borderRadius(16)
            .backgroundColor('#33FFFFFF')
            .border({ width: 1, color: this.isFav ? '#66E7B768' : '#26FFFFFF' })
            .onClick(() => this.toggleFav())
        }
        .width('100%')
        .padding({ left: 16, right: 16, top: 10, bottom: 6 })

        Scroll() {
          Column() {
            Stack({ alignContent: Alignment.BottomStart }) {
              Image(this.item.image)
                .width('100%')
                .height(360)
                .objectFit(ImageFit.Cover)
                .borderRadius(30)

              Column()
                .width('100%')
                .height(360)
                .borderRadius(30)
                .linearGradient({
                  direction: GradientDirection.Bottom,
                  colors: [
                    ['#00000000', 0.35],
                    ['#D906070C', 1.0]
                  ]
                })

              Column() {
                Text(this.item.year)
                  .fontSize(40)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#E6FFFFFF')
                  .letterSpacing(-1)
                Text(this.item.title)
                  .fontSize(25)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#F6F2E9')
                  .margin({ top: 2 })
              }
              .padding({ left: 18, bottom: 16 })
              .alignItems(HorizontalAlign.Start)
            }
            .width('100%')
            .height(360)

            Column() {
              Text(this.item.subtitle)
                .fontSize(11)
                .fontColor(this.item.accent)
                .letterSpacing(0.8)
                .width('100%')
                .margin({ top: 16, bottom: 12 })

              Text(this.item.description)
                .fontSize(14)
                .lineHeight(25)
                .fontColor('#CCF6F2E9')
                .textAlign(TextAlign.JUSTIFY)
                .width('100%')

              Text(`“${this.item.quote}”`)
                .fontSize(13)
                .lineHeight(23)
                .fontColor('#E6F6EBD2')
                .width('100%')
                .padding(14)
                .margin({ top: 18, bottom: 8 })
                .backgroundColor('#14E7B768')
                .border({ width: { left: 2 }, color: '#E7B768' })
                .borderRadius(12)

              Flex({ wrap: FlexWrap.Wrap }) {
                ForEach(this.item.tags, (tag: string) => {
                  this.Tag(tag)
                }, (tag: string) => tag)
              }
              .width('100%')
              .margin({ top: 12 })

              if (this.item.colorway.length > 0) {
                this.MetaRow('配色', this.item.colorway)
              }
              if (this.item.fabric.length > 0) {
                this.MetaRow('面料', this.item.fabric)
              }
              if (this.item.spec.length > 0) {
                this.MetaRow('配置', this.item.spec)
              }
              this.MetaRow('时间', this.item.date)

              Column() {
                Row() {
                  Text('我的回忆手记')
                    .fontSize(12)
                    .fontColor('#D9F6F2E9')
                  Blank()
                  Text(this.status)
                    .fontSize(9)
                    .fontColor('#66F6F2E9')
                }
                .width('100%')

                TextArea({
                  text: this.note,
                  placeholder: '写下你与这段记忆的连接…'
                })
                  .width('100%')
                  .height(118)
                  .fontSize(12)
                  .fontColor('#F6F2E9')
                  .placeholderColor('#4DF6F2E9')
                  .backgroundColor('#14000000')
                  .borderRadius(14)
                  .border({ width: 1, color: '#1FFFFFFF' })
                  .margin({ top: 12, bottom: 10 })
                  .onChange((value: string) => {
                    this.note = value;
                    this.status = '保存中…';
                  })

                Row({ space: 8 }) {
                  Text('保存手记')
                    .fontSize(11)
                    .fontWeight(FontWeight.Bold)
                    .fontColor('#1A1207')
                    .padding({ left: 16, right: 16, top: 9, bottom: 9 })
                    .borderRadius(16)
                    .backgroundColor('#E7B768')
                    .onClick(() => this.saveNote())

                  Text(this.isFav ? '已收藏 ✓' : '收藏这段')
                    .fontSize(11)
                    .fontColor(this.isFav ? '#E7B768' : '#B3F6F2E9')
                    .padding({ left: 16, right: 16, top: 9, bottom: 9 })
                    .borderRadius(16)
                    .backgroundColor('#14FFFFFF')
                    .border({ width: 1, color: this.isFav ? '#66E7B768' : '#26FFFFFF' })
                    .onClick(() => this.toggleFav())
                }
                .width('100%')
              }
              .width('100%')
              .padding(16)
              .margin({ top: 20 })
              .borderRadius(22)
              .backgroundColor('#0FFFFFFF')
              .border({ width: 1, color: '#1FFFFFFF' })

              Text(`${this.item.source} · ${this.item.credit}`)
                .fontSize(9)
                .lineHeight(15)
                .fontColor('#59F6F2E9')
                .width('100%')
                .margin({ top: 16 })

              Row({ space: 10 }) {
                Text('← 上一段')
                  .fontSize(11)
                  .fontColor('#B3F6F2E9')
                  .layoutWeight(1)
                  .height(42)
                  .textAlign(TextAlign.Center)
                  .borderRadius(14)
                  .backgroundColor('#14FFFFFF')
                  .onClick(() => this.step(-1))

                Text('下一段 →')
                  .fontSize(11)
                  .fontColor('#B3F6F2E9')
                  .layoutWeight(1)
                  .height(42)
                  .textAlign(TextAlign.Center)
                  .borderRadius(14)
                  .backgroundColor('#14FFFFFF')
                  .onClick(() => this.step(1))
              }
              .width('100%')
              .margin({ top: 16, bottom: 30 })
            }
            .width('100%')
            .padding({ left: 18, right: 18 })
          }
          .width('100%')
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

