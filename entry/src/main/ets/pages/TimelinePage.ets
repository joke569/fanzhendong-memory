import { router } from '@kit.ArkUI';
import { MEMORIES, getMemories } from '../data/MemoryData';
import { MemoryItem, MemoryLine, lineEn } from '../model/MemoryModels';

@Entry
@Component
struct TimelinePage {
  @State filter: string = 'all';
  @State items: MemoryItem[] = MEMORIES;

  private setFilter(filter: string): void {
    this.filter = filter;
    if (filter === 'all') {
      this.items = MEMORIES;
    } else if (filter === 'jersey') {
      this.items = getMemories(MemoryLine.JERSEY);
    } else if (filter === 'paddle') {
      this.items = getMemories(MemoryLine.PADDLE);
    } else {
      this.items = getMemories(MemoryLine.CAREER);
    }
  }

  @Builder
  FilterChip(label: string, value: string) {
    Text(label)
      .fontSize(11)
      .fontColor(this.filter === value ? '#E7B768' : '#B3F6F2E9')
      .padding({ left: 12, right: 12, top: 7, bottom: 7 })
      .borderRadius(15)
      .backgroundColor(this.filter === value ? '#1FE7B768' : '#14FFFFFF')
      .border({ width: 1, color: this.filter === value ? '#66E7B768' : '#1FFFFFFF' })
      .margin({ right: 7 })
      .onClick(() => this.setFilter(value))
  }

  @Builder
  TimelineRow(item: MemoryItem) {
    Row({ space: 12 }) {
      Image(item.image)
        .width(56)
        .height(66)
        .objectFit(ImageFit.Cover)
        .borderRadius(13)

      Column() {
        Text(`${item.date} · ${lineEn(item.line)}`)
          .fontSize(8)
          .fontColor('#E7B768')
          .letterSpacing(1)
        Text(item.title)
          .fontSize(15)
          .fontWeight(FontWeight.Medium)
          .fontColor('#F6F2E9')
          .margin({ top: 3 })
        Text(item.subtitle)
          .fontSize(10)
          .fontColor('#8CF6F2E9')
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .margin({ top: 2 })
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Text(item.no)
        .fontSize(10)
        .fontColor('#40F6F2E9')
    }
    .width('100%')
    .padding({ top: 10, bottom: 10 })
    .border({ width: { bottom: 1 }, color: '#14FFFFFF' })
    .onClick(() => {
      router.pushUrl({
        url: 'pages/DetailPage',
        params: { id: item.id }
      });
    })
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
          Text('一条时间线')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#F6F2E9')
            .margin({ left: 12 })
        }
        .width('100%')
        .padding({ left: 16, right: 16, top: 12, bottom: 10 })

        Text('把 22 段记忆按时间排好，从第一块球拍到当下。')
          .fontSize(11)
          .fontColor('#8CF6F2E9')
          .width('100%')
          .padding({ left: 18, right: 18 })
          .margin({ bottom: 12 })

        Row() {
          this.FilterChip('全部', 'all')
          this.FilterChip('生涯', 'career')
          this.FilterChip('球衣', 'jersey')
          this.FilterChip('球拍', 'paddle')
        }
        .width('100%')
        .padding({ left: 18, right: 18, bottom: 6 })

        Scroll() {
          Column() {
            ForEach(this.items, (item: MemoryItem) => {
              this.TimelineRow(item)
            }, (item: MemoryItem) => item.id)
          }
          .width('100%')
          .padding({ left: 18, right: 18, bottom: 30 })
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
