// 通用格式化工具：时间、摘要

const pad = (value) => String(value).padStart(2, '0')

// 兼容 "2026-11-22 21:40:00" 与标准 ISO 字符串
export const parseTime = (value) => {
  if (!value) return null
  if (value instanceof Date) return value
  const text = String(value).trim()
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$/.test(text)) {
    return new Date(text.replace(' ', 'T'))
  }
  const date = new Date(text)
  return Number.isNaN(date.getTime()) ? null : date
}

// 相对时间：刚刚 / x 分钟前 / x 小时前 / x 天前 / 日期
export const formatRelativeTime = (value, now = new Date()) => {
  const date = parseTime(value)
  if (!date) return ''

  const diff = now.getTime() - date.getTime()
  if (diff < 60 * 1000) return '刚刚'

  const minutes = Math.floor(diff / (60 * 1000))
  if (minutes < 60) return `${minutes} 分钟前`

  const hours = Math.floor(diff / (60 * 60 * 1000))
  if (hours < 24) return `${hours} 小时前`

  const days = Math.floor(diff / (24 * 60 * 60 * 1000))
  if (days <= 7) return `${days} 天前`

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
}

// 完整时间：2026-11-22 21:40
export const formatDateTime = (value) => {
  const date = parseTime(value)
  if (!date) return ''
  return (
    `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ` +
    `${pad(date.getHours())}:${pad(date.getMinutes())}`
  )
}

// 正文摘要：去掉换行，超长截断
export const toExcerpt = (text, max = 96) => {
  const normalized = String(text || '')
    .replace(/\s+/g, ' ')
    .trim()
  if (normalized.length <= max) return normalized
  return `${normalized.slice(0, max)}…`
}
