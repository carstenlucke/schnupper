/*
  Icon-Register des Themes. Icons kommen aus dem Lucide-Set — dasselbe,
  das auch die Folien des Design-Systems verwenden. Sie werden statisch
  importiert, damit nur die tatsächlich gebrauchten im Bundle landen;
  ein neues Icon also hier eintragen und dann per Name verwenden:
    <Card icon="bot" …>
*/
import type { Component } from 'vue'

import ArrowRight from '~icons/lucide/arrow-right'
import BookOpen from '~icons/lucide/book-open'
import Bot from '~icons/lucide/bot'
import Brain from '~icons/lucide/brain'
import Calculator from '~icons/lucide/calculator'
import Camera from '~icons/lucide/camera'
import ChartLine from '~icons/lucide/chart-line'
import Check from '~icons/lucide/check'
import CircleHelp from '~icons/lucide/circle-help'
import CirclePlay from '~icons/lucide/circle-play'
import ClipboardCheck from '~icons/lucide/clipboard-check'
import Code from '~icons/lucide/code'
import Cog from '~icons/lucide/cog'
import Coins from '~icons/lucide/coins'
import Copy from '~icons/lucide/copy'
import Database from '~icons/lucide/database'
import FolderOpen from '~icons/lucide/folder-open'
import Ghost from '~icons/lucide/ghost'
import GraduationCap from '~icons/lucide/graduation-cap'
import Hash from '~icons/lucide/hash'
import Headphones from '~icons/lucide/headphones'
import Info from '~icons/lucide/info'
import Languages from '~icons/lucide/languages'
import Laptop from '~icons/lucide/laptop'
import Lightbulb from '~icons/lucide/lightbulb'
import ListChecks from '~icons/lucide/list-checks'
import Mail from '~icons/lucide/mail'
import Megaphone from '~icons/lucide/megaphone'
import MessageSquare from '~icons/lucide/message-square'
import MessagesSquare from '~icons/lucide/messages-square'
import Music from '~icons/lucide/music'
import PenLine from '~icons/lucide/pen-line'
import Phone from '~icons/lucide/phone'
import Plug from '~icons/lucide/plug'
import Quote from '~icons/lucide/quote'
import RefreshCw from '~icons/lucide/refresh-cw'
import Rocket from '~icons/lucide/rocket'
import ScanSearch from '~icons/lucide/scan-search'
import SearchCheck from '~icons/lucide/search-check'
import ShieldCheck from '~icons/lucide/shield-check'
import Smartphone from '~icons/lucide/smartphone'
import Smile from '~icons/lucide/smile'
import Target from '~icons/lucide/target'
import TrendingUp from '~icons/lucide/trending-up'
import UserCog from '~icons/lucide/user-cog'
import Users from '~icons/lucide/users'
import Wrench from '~icons/lucide/wrench'
import X from '~icons/lucide/x'
import Zap from '~icons/lucide/zap'

export const icons: Record<string, Component> = {
  'arrow-right': ArrowRight,
  'book-open': BookOpen,
  'bot': Bot,
  'brain': Brain,
  'calculator': Calculator,
  'camera': Camera,
  'chart-line': ChartLine,
  'check': Check,
  'circle-help': CircleHelp,
  'circle-play': CirclePlay,
  'clipboard-check': ClipboardCheck,
  'code': Code,
  'cog': Cog,
  'coins': Coins,
  'copy': Copy,
  'database': Database,
  'folder-open': FolderOpen,
  'ghost': Ghost,
  'graduation-cap': GraduationCap,
  'hash': Hash,
  'headphones': Headphones,
  'info': Info,
  'languages': Languages,
  'laptop': Laptop,
  'lightbulb': Lightbulb,
  'list-checks': ListChecks,
  'mail': Mail,
  'megaphone': Megaphone,
  'message-square': MessageSquare,
  'messages-square': MessagesSquare,
  'music': Music,
  'pen-line': PenLine,
  'phone': Phone,
  'plug': Plug,
  'quote': Quote,
  'refresh-cw': RefreshCw,
  'rocket': Rocket,
  'scan-search': ScanSearch,
  'search-check': SearchCheck,
  'shield-check': ShieldCheck,
  'smartphone': Smartphone,
  'smile': Smile,
  'target': Target,
  'trending-up': TrendingUp,
  'user-cog': UserCog,
  'users': Users,
  'wrench': Wrench,
  'x': X,
  'zap': Zap,
}
