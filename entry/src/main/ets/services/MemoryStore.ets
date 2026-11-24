import { preferences } from '@kit.ArkData';
import { common } from '@kit.AbilityKit';
import { MemoryState } from '../model/MemoryModels';

function parseArray(raw: string): string[] {
  try {
    const value: string[] = JSON.parse(raw) as string[];
    return value;
  } catch (e) {
    return [];
  }
}

export class MemoryStore {
  private static pref: preferences.Preferences | null = null;

  static async init(context: common.UIAbilityContext): Promise<void> {
    if (MemoryStore.pref === null) {
      MemoryStore.pref = await preferences.getPreferences(context, 'fzd_memory');
    }
  }

  static async load(): Promise<MemoryState> {
    const state = new MemoryState();
    if (MemoryStore.pref === null) {
      return state;
    }
    const favorites = await MemoryStore.pref.get('favorites', '[]');
    const visited = await MemoryStore.pref.get('visited', '[]');
    const lastId = await MemoryStore.pref.get('lastId', '');
    const lastLine = await MemoryStore.pref.get('lastLine', 'all');
    const reduceMotion = await MemoryStore.pref.get('reduceMotion', false);
    state.favorites = parseArray(String(favorites));
    state.visited = parseArray(String(visited));
    state.lastId = String(lastId);
    state.lastLine = String(lastLine);
    state.reduceMotion = Boolean(reduceMotion);
    return state;
  }

  static async saveState(state: MemoryState): Promise<void> {
    if (MemoryStore.pref === null) {
      return;
    }
    await MemoryStore.pref.put('favorites', JSON.stringify(state.favorites));
    await MemoryStore.pref.put('visited', JSON.stringify(state.visited));
    await MemoryStore.pref.put('lastId', state.lastId);
    await MemoryStore.pref.put('lastLine', state.lastLine);
    await MemoryStore.pref.put('reduceMotion', state.reduceMotion);
    await MemoryStore.pref.flush();
  }

  static async getNote(id: string): Promise<string> {
    if (MemoryStore.pref === null) {
      return '';
    }
    const value = await MemoryStore.pref.get('note_' + id, '');
    return String(value);
  }

  static async saveNote(id: string, note: string): Promise<void> {
    if (MemoryStore.pref === null) {
      return;
    }
    await MemoryStore.pref.put('note_' + id, note);
    await MemoryStore.pref.flush();
  }

  static async clearAll(): Promise<void> {
    if (MemoryStore.pref === null) {
      return;
    }
    await MemoryStore.pref.clear();
    await MemoryStore.pref.flush();
  }
}
