import { MemoryItem, lineEn } from '../model/MemoryModels';
import { MEMORIES } from '../data/MemoryData';

@Component
export struct MemoryPoster {
  @Prop item: MemoryItem = MEMORIES[0];
  @Prop isFavorite: boolean = false;
  @Prop reduceMotion: boolean = false;
  onOpen: () => void = () => {};

  build() {
    Stack({ alignContent: Alignment.TopStart }) {
      Image(this.item.image)
        .width('100%')
        .height('100%')
        .objectFit(ImageFit.Cover)

      Column()
        .width('100%')
        .height('100%')
        .linearGradient({
          direction: GradientDirection.Bottom,
          colors: [
            ['#66000000', 0.0],
            ['#00000000', 0.32],
            ['#00000000', 0.48],
            ['#E6000000', 1.0]
          ]
        })

      Row() {
        Text(lineEn(this.item.line))
          .fontSize(9)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.item.accent)
          .letterSpacing(1.8)
          .padding({ left: 10, right: 10, top: 6, bottom: 6 })
          .borderRadius(14)
          .backgroundColor('#4D0C0E14')
          .border({ width: 1, color: '#33FFFFFF' })

        Text(this.item.date)
          .fontSize(9)
          .fontColor('#CCF6F2E9')
          .padding({ left: 10, right: 10, top: 6, bottom: 6 })
          .borderRadius(14)
          .backgroundColor('#4D0C0E14')
          .border({ width: 1, color: '#26FFFFFF' })
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 16 })
      .justifyContent(FlexAlign.SpaceBetween)

      Text(this.isFavorite ? '♥' : '♡')
        .fontSize(22)
        .fontColor(this.isFavorite ? '#E7B768' : '#F6F2E9')
        .width(36)
        .height(36)
        .textAlign(TextAlign.Center)
        .borderRadius(18)
        .backgroundColor('#4D0C0E14')
        .border({ width: 1, color: '#33FFFFFF' })
        .position({ x: '87%', y: 54 })

      Column() {
        Text(this.item.year)
          .fontSize(54)
          .fontWeight(FontWeight.Bold)
          .fontColor('#F2FFFFFF')
          .letterSpacing(-2)

        Text(this.item.title)
          .fontSize(28)
          .fontWeight(FontWeight.Bold)
          .fontColor('#F6F2E9')
          .margin({ top: 6 })

        Text(this.item.subtitle)
          .fontSize(12)
          .fontColor('#B3F6F2E9')
          .margin({ top: 4, bottom: 12 })

        Marquee({
          start: !this.reduceMotion,
          step: 5,
          loop: -1,
          fromStart: true,
          src: this.item.caption
        })
          .width('100%')
          .height(30)
          .fontSize(10)
          .fontColor('#CCF6F2E9')
          .backgroundColor('#4D0A0C12')
          .borderRadius(15)
      }
      .width('100%')
      .alignItems(HorizontalAlign.Start)
      .padding({ left: 20, right: 20, bottom: 20 })
      .position({ x: 0, y: '64%' })
    }
    .width('100%')
    .height('100%')
    .borderRadius(34)
    .clip(true)
    .backgroundColor('#12141C')
    .border({ width: 1, color: '#33FFFFFF' })
    .shadow({ radius: 30, color: '#66000000', offsetX: 0, offsetY: 18 })
    .onClick(() => {
      this.onOpen();
    })
  }
}
