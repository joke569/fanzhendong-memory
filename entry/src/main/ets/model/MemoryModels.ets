export enum MemoryLine {
  CAREER = 'career',
  JERSEY = 'jersey',
  PADDLE = 'paddle'
}

export class MemoryItem {
  id: string;
  line: MemoryLine;
  no: string;
  year: string;
  date: string;
  title: string;
  subtitle: string;
  caption: string;
  description: string;
  quote: string;
  tags: string[];
  image: Resource;
  accent: string;
  colorway: string;
  fabric: string;
  spec: string;
  source: string;
  credit: string;

  constructor(id: string, line: MemoryLine, no: string, year: string, date: string, title: string,
    subtitle: string, caption: string, description: string, quote: string, tags: string[],
    image: Resource, accent: string, colorway: string, fabric: string, spec: string,
    source: string, credit: string) {
    this.id = id;
    this.line = line;
    this.no = no;
    this.year = year;
    this.date = date;
    this.title = title;
    this.subtitle = subtitle;
    this.caption = caption;
    this.description = description;
    this.quote = quote;
    this.tags = tags;
    this.image = image;
    this.accent = accent;
    this.colorway = colorway;
    this.fabric = fabric;
    this.spec = spec;
    this.source = source;
    this.credit = credit;
  }
}

export function lineLabel(line: MemoryLine): string {
  if (line === MemoryLine.CAREER) {
    return '生涯';
  }
  if (line === MemoryLine.JERSEY) {
    return '球衣';
  }
  return '球拍';
}

export function lineEn(line: MemoryLine): string {
  if (line === MemoryLine.CAREER) {
    return 'CAREER';
  }
  if (line === MemoryLine.JERSEY) {
    return 'JERSEY';
  }
  return 'PADDLE';
}

export function lineAccent(line: MemoryLine): string {
  if (line === MemoryLine.CAREER) {
    return '#E7B768';
  }
  if (line === MemoryLine.JERSEY) {
    return '#D24A4E';
  }
  return '#59B89A';
}

export interface DetailParams {
  id: string;
}

export class MemoryState {
  favorites: string[] = [];
  lastId: string = '';
  lastLine: string = 'all';
  reduceMotion: boolean = false;
  visited: string[] = [];

  isFavorite(id: string): boolean {
    return this.favorites.indexOf(id) >= 0;
  }

  toggleFavorite(id: string): boolean {
    const index = this.favorites.indexOf(id);
    if (index >= 0) {
      this.favorites.splice(index, 1);
      return false;
    }
    this.favorites.push(id);
    return true;
  }

  markVisited(id: string): void {
    if (this.visited.indexOf(id) < 0) {
      this.visited.push(id);
    }
  }
}
