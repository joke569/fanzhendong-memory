import { router, promptAction } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';
import { MEMORIES, getMemories } from '../data/MemoryData';
import { MemoryItem, MemoryLine, MemoryState, lineEn } from '../model/MemoryModels';
import { MemoryStore } from '../services/MemoryStore';
import { MemoryPoster } from '../components/MemoryPoster';
import { LineDock } from '../components/LineDock';

@Entry
@Component
struct Index {
  @State items: MemoryItem[] = MEMORIES;
  @State currentIndex: number = 0;
  @State activeLine: string = 'all';
  @State favorites: string[] = [];
  @State visited: string[] = [];
  @State reduceMotion: boolean = false;
  @State loaded: boolean = false;
  private swiperController: SwiperController = new SwiperController();

  aboutToAppear(): void {
    this.initData();
  }

  onPageShow(): void {
    if (this.loaded) {
      this.refreshFavorites();
    }
  }

  async initData(): Promise<void> {
    const context = getContext(this) as common.UIAbilityContext;
    await MemoryStore.init(context);
    const state = await MemoryStore.load();
    this.favorites = state.favorites;
    this.visited = state.visited;
    this.reduceMotion = state.reduceMotion;
    this.activeLine = state.lastLine;
    if (this.activeLine === 'career' || this.activeLine === 'jersey' || this.activeLine === 'paddle') {
      this.items = getMemories(this.lineEnum(this.activeLine));
    } else {
      this.activeLine = 'all';
      this.items = MEMORIES;
    }
    let index = 0;
    if (state.lastId.length > 0) {
      const found = this.items.findIndex((item: MemoryItem) => item.id === state.lastId);
      if (found >= 0) {
        index = found;
      }
    }
    this.currentIndex = index;
    this.loaded = true;
    this.swiperController.changeIndex(index, false);
    if (state.lastId.length > 0) {
      promptAction.showToast({ message: '已恢复上次回忆', duration: 1600 });
    }
  }

  async refreshFavorites(): Promise<void> {
    const state = await MemoryStore.load();
    this.favorites = state.favorites;
    this.reduceMotion = state.reduceMotion;
  }

  private lineEnum(line: string): MemoryLine {
    if (line === 'jersey') {
      return MemoryLine.JERSEY;
    }
    if (line === 'paddle') {
      return MemoryLine.PADDLE;
    }
    return MemoryLine.CAREER;
  }

  private getCurrentItem(): MemoryItem {
    if (this.items.length === 0) {
      return MEMORIES[0];
    }
    const index = Math.min(Math.max(this.currentIndex, 0), this.items.length - 1);
    return this.items[index];
  }

  private isFavorite(id: string): boolean {
    return this.favorites.indexOf(id) >= 0;
  }

  private selectFilter(line: string): void {
    this.activeLine = line;
    if (line === 'all') {
      this.items = MEMORIES;
    } else {
      this.items = getMemories(this.lineEnum(line));
    }
    this.currentIndex = 0;
    this.swiperController.changeIndex(0, false);
    this.persist();
  }

  private selectItem(item: MemoryItem): void {
    let index = this.items.findIndex((it: MemoryItem) => it.id === item.id);
    if (index < 0) {
      this.activeLine = 'all';
      this.items = MEMORIES;
      index = this.items.findIndex((it: MemoryItem) => it.id === item.id);
    }
    if (index >= 0) {
      this.currentIndex = index;
      this.swiperController.changeIndex(index, false);
      this.persist();
    }
  }

  private openDetail(item: MemoryItem): void {
    this.persist();
    router.pushUrl({
      url: 'pages/DetailPage',
      params: { id: item.id }
    });
  }

  private openTimeline(): void {
    router.pushUrl({ url: 'pages/TimelinePage' });
  }

  private openSettings(): void {
    router.pushUrl({ url: 'pages/SettingsPage' });
  }

  private makeState(): MemoryState {
    const state = new MemoryState();
    state.favorites = this.favorites;
    state.visited = this.visited;
    state.reduceMotion = this.reduceMotion;
    state.lastLine = this.activeLine;
    state.lastId = this.getCurrentItem().id;
    return state;
  }

  private persist(): void {
    MemoryStore.saveState(this.makeState());
  }

  @Builder
  Header() {
    Row() {
      Column() {
        Text('樊振东')
          .fontSize(21)
          .fontWeight(FontWeight.Bold)
          .fontColor('#F6F2E9')
          .letterSpacing(1)
        Text('三线回忆录 / MEMORY ARCHIVE')
          .fontSize(8)
          .fontColor('#8CF6F2E9')
          .letterSpacing(1.2)
          .margin({ top: 3 })
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      Text('全部')
        .fontSize(10)
        .fontColor(this.activeLine === 'all' ? '#E7B768' : '#B3F6F2E9')
        .padding({ left: 10, right: 10, top: 6, bottom: 6 })
        .borderRadius(14)
        .backgroundColor('#26FFFFFF')
        .border({ width: 1, color: this.activeLine === 'all' ? '#66E7B768' : '#26FFFFFF' })
        .margin({ right: 6 })
        .onClick(() => this.selectFilter('all'))

      Text(`${(this.currentIndex + 1).toString().padStart(2, '0')} / ${this.items.length.toString().padStart(2, '0')}`)
        .fontSize(9)
        .fontColor('#E7B768')
        .padding({ left: 9, right: 9, top: 6, bottom: 6 })
        .borderRadius(14)
        .backgroundColor('#26FFFFFF')
        .border({ width: 1, color: '#26FFFFFF' })
        .margin({ right: 6 })

      Text('≡')
        .fontSize(19)
        .fontColor('#D9F6F2E9')
        .width(32)
        .height(32)
        .textAlign(TextAlign.Center)
        .borderRadius(16)
        .backgroundColor('#26FFFFFF')
        .border({ width: 1, color: '#26FFFFFF' })
        .margin({ right: 5 })
        .onClick(() => this.openTimeline())

      Text('⚙')
        .fontSize(16)
        .fontColor('#D9F6F2E9')
        .width(32)
        .height(32)
        .textAlign(TextAlign.Center)
        .borderRadius(16)
        .backgroundColor('#26FFFFFF')
        .border({ width: 1, color: '#26FFFFFF' })
        .onClick(() => this.openSettings())
    }
    .width('100%')
    .padding({ left: 18, right: 16, top: 12, bottom: 6 })
    .alignItems(VerticalAlign.Center)
  }

  @Builder
  Filmstrip() {
    Scroll() {
      Row({ space: 8 }) {
        ForEach(MEMORIES, (item: MemoryItem) => {
          Image(item.image)
            .width(48)
            .height(64)
            .objectFit(ImageFit.Cover)
            .borderRadius(12)
            .opacity(this.getCurrentItem().id === item.id ? 1 : 0.52)
            .border({
              width: 1,
              color: this.getCurrentItem().id === item.id ? item.accent : '#26FFFFFF'
            })
            .onClick(() => this.selectItem(item))
        }, (item: MemoryItem) => item.id)
      }
      .padding({ left: 18, right: 18 })
    }
    .width('100%')
    .height(78)
    .scrollable(ScrollDirection.Horizontal)
    .scrollBar(BarState.Off)
  }

  build() {
    Stack({ alignContent: Alignment.Bottom }) {
      Image(this.getCurrentItem().image)
        .width('100%')
        .height('100%')
        .objectFit(ImageFit.Cover)
        .blur(50)
        .opacity(0.26)

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
        this.Header()

        Swiper(this.swiperController) {
          ForEach(this.items, (item: MemoryItem) => {
            MemoryPoster({
              item: item,
              isFavorite: this.isFavorite(item.id),
              reduceMotion: this.reduceMotion,
              onOpen: () => this.openDetail(item)
            })
              .width('100%')
              .height('100%')
          }, (item: MemoryItem) => item.id)
        }
        .index(this.currentIndex)
        .loop(true)
        .vertical(true)
        .autoPlay(!this.reduceMotion)
        .interval(6500)
        .duration(700)
        .indicator(false)
        .width('100%')
        .layoutWeight(1)
        .padding({ left: 16, right: 16, top: 6, bottom: 4 })
        .onChange((index: number) => {
          this.currentIndex = index;
          this.persist();
        })

        this.Filmstrip()

        Blank().height(84)
      }
      .width('100%')
      .height('100%')

      Row() {
        LineDock({
          activeLine: this.activeLine,
          onSelect: (line: string) => this.selectFilter(line)
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .margin({ bottom: 12 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#06070C')
  }
}
