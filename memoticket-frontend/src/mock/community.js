// ============================================================
// 社区与体验分享 —— 本地演示数据
// ------------------------------------------------------------
// 后端 /api/community/* 接口就绪前，src/api/community.js 会从这里
// 取数据，保证页面可以直接演示。数据写在 localStorage 中，
// 因此点赞、评论、发布在刷新后依然保留。
// 后端接口就绪后，把 api/community.js 里的 COMMUNITY_DEMO_MODE
// 改为 false 即可无缝切换，本文件可以整删。
// ============================================================

const STORAGE_KEY = 'memoticket_community_demo_v2'

// 演示用的兴趣分类（真实环境由 /api/interests 提供）
export const DEMO_INTERESTS = [
  { id: 1, name: '二次元动漫', icon: '🎌' },
  { id: 2, name: '独立游戏', icon: '🎮' },
  { id: 3, name: '户外徒步', icon: '🥾' },
  { id: 4, name: '科幻电影', icon: '🚀' },
  { id: 5, name: '现场音乐', icon: '🎧' },
  { id: 6, name: '展览与艺术', icon: '🖼️' },
  { id: 7, name: '剧本杀与密室', icon: '🕵️' }
]

// 演示用的票夹数据，用于发布页「关联票根」下拉框
export const DEMO_TICKETS = [
  {
    id: 1,
    title: '《奥本海默》',
    type: '电影',
    rating: 5,
    eventDate: '2026-11-01',
    venue: '万达影城 IMAX 厅'
  },
  {
    id: 2,
    title: '《青川怪谈》',
    type: '剧本杀',
    rating: 4,
    eventDate: '2026-11-10',
    venue: '迷之屋'
  },
  {
    id: 3,
    title: '《Stray》',
    type: '游戏',
    rating: 5,
    eventDate: '2026-11-15',
    venue: '家里'
  }
]

const seedShares = () => [
  {
    id: 1,
    title: 'IMAX 二刷《奥本海默》：声音先于画面击中我',
    content:
      '第一次看是在普通厅，第二次特意抢了 IMAX 早场。真正把我按在座椅上的是声音：低频从脚底往上推，核爆那一段反而安静得可怕。\n\n诺兰把三个小时切成三条时间线，黑白与彩色交替，像两套不同的记忆在互相校对。二刷时我才注意到，奥本海默每一次眨眼，都对应一次审判视角的切换。\n\n如果你打算去看，建议提前半小时进场，别带爆米花——这部片子需要一点安静。',
    author: { id: 12, nickname: '胶片旅人', color: '#6c5ce7' },
    interestId: 4,
    interestName: '科幻电影',
    rating: 5,
    tags: ['IMAX', '诺兰', '二刷'],
    images: [],
    ticket: {
      id: 1,
      title: '《奥本海默》',
      type: '电影',
      eventDate: '2026-11-01',
      venue: '万达影城 IMAX 厅'
    },
    likeCount: 128,
    favoriteCount: 64,
    commentCount: 3,
    createTime: '2026-11-22 21:40:00'
  },
  {
    id: 2,
    title: '徽杭古道 18 公里：秋天是这条线最好的滤镜',
    content:
      '从安徽绩溪走到浙江临安，全程约 18 公里，秋天是最好的季节。\n\n早上六点出发，石阶上还挂着露水，走到蓝天凹时云刚好散开。中途在古道人家吃了一碗笋干面，10 块钱，热气腾腾。\n\n装备提示：登山杖真的有用，下坡保护膝盖；山顶风大，冲锋衣别嫌重；全程没有补给点，水至少带 1.5L。',
    author: { id: 23, nickname: '山系青年', color: '#00b894' },
    interestId: 3,
    interestName: '户外徒步',
    rating: 4,
    tags: ['徽杭古道', '轻装徒步', '秋色'],
    images: [],
    ticket: null,
    likeCount: 96,
    favoriteCount: 51,
    commentCount: 1,
    createTime: '2026-11-20 19:05:00'
  },
  {
    id: 3,
    title: '《Stray》：一只橘猫把我带回赛博朋克的深夜',
    content:
      '《Stray》是一款你扮演橘猫的冒险游戏，但它真正的主角是那座没有人类的赛博城市。\n\n开局十分钟我就放弃了「通关」的念头，只想沿着霓虹灯慢慢走，把每一扇窗都看一遍。机器人 NPC 的孤独感写得很克制，没有一句台词是多余的。\n\n唯一的问题是第一小时容易劝退：操作手感偏钝，谜题节奏也慢。熬过去之后，它会给你一个非常温柔的后半程。',
    author: { id: 31, nickname: '像素猫', color: '#e17055' },
    interestId: 2,
    interestName: '独立游戏',
    rating: 5,
    tags: ['独立游戏', '赛博朋克', '猫咪'],
    images: [],
    ticket: {
      id: 3,
      title: '《Stray》',
      type: '游戏',
      eventDate: '2026-11-15',
      venue: '家里'
    },
    likeCount: 210,
    favoriteCount: 133,
    commentCount: 2,
    createTime: '2026-11-18 23:15:00'
  },
  {
    id: 4,
    title: '上海双年展：把整个展厅当成一座城市来逛',
    content:
      '今年的双年展把整个西岸美术馆当成一座城市来布置，展厅之间用「街道」连接。\n\n最喜欢的是一楼那件声音装置：观众走进去，脚步声会触发不同的广播片段，像是在偷听别人的日常。建议工作日下午去，人少的时候才能真正听见。\n\n门票 60 元，学生半价，地铁 11 号线云锦路站步行 10 分钟。',
    author: { id: 18, nickname: '看展不看说明', color: '#0984e3' },
    interestId: 6,
    interestName: '展览与艺术',
    rating: 4,
    tags: ['双年展', '声音装置', '西岸'],
    images: [],
    ticket: null,
    likeCount: 74,
    favoriteCount: 39,
    commentCount: 1,
    createTime: '2026-11-16 15:30:00'
  },
  {
    id: 5,
    title: '草东没有派对 Livehouse：灯一灭，地板就开始震',
    content:
      '草东的现场不需要暖场，灯一灭人群就开始喊。\n\n《山海》前奏响起的时候，整个 Livehouse 的地板都在震。主唱几乎不讲话，一首接一首地唱，安可只返了一首《大风吹》。\n\n小场地的好处是能看清每个人的表情，坏处是站两个小时腿真的会废。下次一定穿运动鞋。',
    author: { id: 27, nickname: '站票选手', color: '#e84393' },
    interestId: 5,
    interestName: '现场音乐',
    rating: 5,
    tags: ['Livehouse', '草东', '安可'],
    images: [],
    ticket: null,
    likeCount: 156,
    favoriteCount: 47,
    commentCount: 2,
    createTime: '2026-11-14 23:50:00'
  },
  {
    id: 6,
    title: '《蓦然回首》重映：画格之间藏着一整个青春',
    content:
      '《蓦然回首》重映，第四次看，还是在同一个镜头哭了。\n\n藤本树把「如果当初」画成了两条平行线，两个女孩在各自的房间里画画，背影几乎一样。动画版加的雨中奔跑那段，把原作的留白补得很温柔。\n\n片长不到一小时，但散场后在座位上坐了很久。',
    author: { id: 35, nickname: '一格一格', color: '#f39c12' },
    interestId: 1,
    interestName: '二次元动漫',
    rating: 4,
    tags: ['藤本树', '重映', '动画'],
    images: [],
    ticket: null,
    likeCount: 61,
    favoriteCount: 28,
    commentCount: 1,
    createTime: '2026-11-11 21:10:00'
  },
  {
    id: 7,
    title: '《青川怪谈》四小时：恐怖不靠吓，靠「你确定你记得吗」',
    content:
      '《青川怪谈》是民国恐怖本，四人开，时长四小时。\n\n恐怖感不靠 jump scare，靠的是本子里那些「你确定你记得」的细节。第二幕开始每个人都开始怀疑自己的记忆，DM 的节奏控得很好，没有为了吓人硬加环节。\n\n避雷：文字量不小，怕读本的朋友慎入；不过对新手相对友好，第一次玩剧本杀也能跟上。',
    author: { id: 41, nickname: '本格推理迷', color: '#6c5ce7' },
    interestId: 7,
    interestName: '剧本杀与密室',
    rating: 4,
    tags: ['剧本杀', '民国恐怖', '四人本'],
    images: [],
    ticket: {
      id: 2,
      title: '《青川怪谈》',
      type: '剧本杀',
      eventDate: '2026-11-10',
      venue: '迷之屋'
    },
    likeCount: 88,
    favoriteCount: 42,
    commentCount: 0,
    createTime: '2026-11-09 22:35:00'
  }
]

const seedComments = () => ({
  1: [
    {
      id: 1,
      author: { nickname: '白噪音收藏家', color: '#0984e3' },
      content: '「低频从脚底往上推」太准确了，我看的时候全程攥着扶手。',
      createTime: '2026-11-22 22:10:00'
    },
    {
      id: 2,
      author: { nickname: '诺兰编年史', color: '#6c5ce7' },
      content: '二刷确实能看出很多细节，尤其是黑白线里的那场审判。',
      createTime: '2026-11-23 09:15:00'
    },
    {
      id: 3,
      author: { nickname: '橙子汽水', color: '#e17055' },
      content: '建议很实在，我上次带了大桶爆米花，全程不敢嚼。',
      createTime: '2026-11-23 20:02:00'
    }
  ],
  2: [
    {
      id: 4,
      author: { nickname: '周末野人', color: '#00b894' },
      content: '蓝天凹的云海值得早起，我上次去全是雾，什么也没看到。',
      createTime: '2026-11-21 08:02:00'
    }
  ],
  3: [
    {
      id: 5,
      author: { nickname: '深夜放毒', color: '#e84393' },
      content: '赛博城市的设计真的绝，我为了看广告牌在巷子里转了半小时。',
      createTime: '2026-11-19 11:20:00'
    },
    {
      id: 6,
      author: { nickname: '手柄收藏家', color: '#f39c12' },
      content: '第一小时确实差点弃游，幸好坚持下来了。',
      createTime: '2026-11-19 23:41:00'
    }
  ],
  4: [
    {
      id: 7,
      author: { nickname: '美术馆钉子户', color: '#6c5ce7' },
      content: '声音装置那件我也喜欢，可惜周末人太多，听不清。',
      createTime: '2026-11-17 16:20:00'
    }
  ],
  5: [
    {
      id: 8,
      author: { nickname: '音浪太强', color: '#0984e3' },
      content: '上次草东现场也是这首安可，鸡皮疙瘩。',
      createTime: '2026-11-15 01:12:00'
    },
    {
      id: 9,
      author: { nickname: '在场证明', color: '#00b894' },
      content: '穿运动鞋这条建议应该置顶。',
      createTime: '2026-11-15 12:30:00'
    }
  ],
  6: [
    {
      id: 10,
      author: { nickname: '画格搬运工', color: '#e17055' },
      content: '雨中奔跑那段补得刚刚好，原作留白变成了呼吸。',
      createTime: '2026-11-12 21:05:00'
    }
  ],
  7: []
})

const seedState = () => ({
  shares: seedShares(),
  comments: seedComments(),
  likedIds: [],
  favoritedIds: [],
  nextShareId: 100,
  nextCommentId: 101
})

// ---------------- 本地存储 ----------------

let state = null

const load = () => {
  if (state) return state
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const parsed = raw ? JSON.parse(raw) : null
    if (parsed && Array.isArray(parsed.shares)) {
      state = parsed
      return state
    }
  } catch (error) {
    console.warn('[社区演示数据] 读取本地缓存失败，将使用初始数据', error)
  }
  state = seedState()
  save()
  return state
}

const save = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  } catch (error) {
    console.warn('[社区演示数据] 写入本地缓存失败', error)
  }
}

// ---------------- 查询辅助 ----------------

const pad = (value) => String(value).padStart(2, '0')

const formatNow = () => {
  const now = new Date()
  return (
    `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ` +
    `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
  )
}

const currentUser = () => {
  const userId = Number(localStorage.getItem('user_id')) || 0
  return {
    id: userId,
    nickname: localStorage.getItem('nickname') || '我'
  }
}

const toCard = (share) => {
  const data = load()
  return {
    ...share,
    liked: data.likedIds.includes(share.id),
    favorited: data.favoritedIds.includes(share.id)
  }
}

const hotScore = (share) => share.likeCount * 2 + share.commentCount * 5 + share.favoriteCount

// ---------------- 对外查询 ----------------

export const demoOverview = () => {
  const data = load()
  const hot = [...data.shares].sort((a, b) => hotScore(b) - hotScore(a)).slice(0, 4)
  return {
    stats: {
      shareCount: 1200 + data.shares.length,
      interestCount: DEMO_INTERESTS.length,
      authorCount: 573,
      commentCount: 2864
    },
    interests: DEMO_INTERESTS.map((item) => ({
      ...item,
      shareCount: data.shares.filter((share) => share.interestId === item.id).length
    })),
    hot: hot.map(toCard)
  }
}

export const demoFeed = ({ interestId = '', sort = 'latest', keyword = '', page = 1, pageSize = 5 } = {}) => {
  const data = load()
  let list = [...data.shares]

  if (interestId) {
    list = list.filter((share) => share.interestId === Number(interestId))
  }

  const trimmed = String(keyword || '').trim().toLowerCase()
  if (trimmed) {
    list = list.filter((share) => {
      const haystack = [share.title, share.content, share.interestName, ...(share.tags || [])]
        .join(' ')
        .toLowerCase()
      return haystack.includes(trimmed)
    })
  }

  if (sort === 'hot') {
    list.sort((a, b) => hotScore(b) - hotScore(a))
  } else {
    list.sort((a, b) => String(b.createTime).localeCompare(String(a.createTime)))
  }

  const total = list.length
  const size = Math.max(1, Number(pageSize) || 5)
  const current = Math.max(1, Number(page) || 1)
  const start = (current - 1) * size

  return {
    list: list.slice(start, start + size).map(toCard),
    total,
    page: current,
    pageSize: size
  }
}

export const demoShareDetail = (id) => {
  const data = load()
  const share = data.shares.find((item) => item.id === Number(id))
  if (!share) return null
  return toCard(share)
}

export const demoComments = (id) => {
  const data = load()
  return data.comments[Number(id)] || []
}

// ---------------- 写操作 ----------------

export const demoToggleLike = (id) => {
  const data = load()
  const share = data.shares.find((item) => item.id === Number(id))
  if (!share) return null

  const index = data.likedIds.indexOf(share.id)
  if (index >= 0) {
    data.likedIds.splice(index, 1)
    share.likeCount = Math.max(0, share.likeCount - 1)
  } else {
    data.likedIds.push(share.id)
    share.likeCount += 1
  }
  save()
  return toCard(share)
}

export const demoToggleFavorite = (id) => {
  const data = load()
  const share = data.shares.find((item) => item.id === Number(id))
  if (!share) return null

  const index = data.favoritedIds.indexOf(share.id)
  if (index >= 0) {
    data.favoritedIds.splice(index, 1)
    share.favoriteCount = Math.max(0, share.favoriteCount - 1)
  } else {
    data.favoritedIds.push(share.id)
    share.favoriteCount += 1
  }
  save()
  return toCard(share)
}

export const demoAddComment = (id, content) => {
  const data = load()
  const share = data.shares.find((item) => item.id === Number(id))
  if (!share) return null

  const comment = {
    id: data.nextCommentId++,
    author: currentUser(),
    content: String(content || '').trim(),
    createTime: formatNow()
  }

  if (!data.comments[share.id]) data.comments[share.id] = []
  data.comments[share.id].push(comment)
  share.commentCount += 1
  save()
  return comment
}

export const demoCreateShare = (payload) => {
  const data = load()
  const interest = DEMO_INTERESTS.find((item) => item.id === Number(payload.interestId))
  const ticket = payload.ticketId
    ? DEMO_TICKETS.find((item) => item.id === Number(payload.ticketId))
    : null

  const share = {
    id: data.nextShareId++,
    title: String(payload.title || '').trim(),
    content: String(payload.content || '').trim(),
    author: currentUser(),
    interestId: interest ? interest.id : null,
    interestName: interest ? interest.name : '未分类',
    rating: Number(payload.rating) || 5,
    tags: Array.isArray(payload.tags) ? payload.tags.slice(0, 5) : [],
    images: Array.isArray(payload.images) ? payload.images.filter(Boolean).slice(0, 3) : [],
    ticket: ticket
      ? {
          id: ticket.id,
          title: ticket.title,
          type: ticket.type,
          eventDate: ticket.eventDate,
          venue: ticket.venue
        }
      : null,
    likeCount: 0,
    favoriteCount: 0,
    commentCount: 0,
    createTime: formatNow()
  }

  data.shares.unshift(share)
  data.comments[share.id] = []
  save()
  return toCard(share)
}

// 演示环境下清空本地数据，方便反复验证首发效果
export const demoReset = () => {
  state = seedState()
  save()
}
