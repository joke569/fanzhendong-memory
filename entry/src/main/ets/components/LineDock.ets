import { MemoryLine, lineLabel, lineEn } from '../model/MemoryModels';

@Component
export struct LineDock {
  @Prop activeLine: string = 'all';
  onSelect: (line: string) => void = () => {};

  @Builder
  DockItem(line: string, no: string, label: string, en: string) {
    Column() {
      Text(no)
        .fontSize(7)
        .fontColor(this.activeLine === line ? '#B3E7B768' : '#59FFFFFF')
        .letterSpacing(1.2)
      Text(label)
        .fontSize(13)
        .fontWeight(FontWeight.Medium)
        .fontColor(this.activeLine === line ? '#F6F2E9' : '#B3F6F2E9')
        .margin({ top: 1 })
      Text(en)
        .fontSize(7)
        .fontColor(this.activeLine === line ? '#B3E7B768' : '#59FFFFFF')
        .letterSpacing(1.4)
        .margin({ top: 1 })
    }
    .layoutWeight(1)
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .borderRadius(22)
    .backgroundColor(this.activeLine === line ? '#1FE7B768' : '#00000000')
    .border({
      width: 1,
      color: this.activeLine === line ? '#47E7B768' : '#00FFFFFF'
    })
    .onClick(() => {
      this.onSelect(line);
    })
  }

  build() {
    Row({ space: 6 }) {
      this.DockItem('career', '01', '生涯', 'CAREER')
      this.DockItem('jersey', '02', '球衣', 'JERSEY')
      this.DockItem('paddle', '03', '球拍', 'PADDLE')
    }
    .width('92%')
    .height(70)
    .padding(6)
    .borderRadius(28)
    .backgroundColor('#CC12141C')
    .backdropBlur(24)
    .border({ width: 1, color: '#26FFFFFF' })
    .shadow({ radius: 30, color: '#66000000', offsetX: 0, offsetY: 16 })
  }
}
