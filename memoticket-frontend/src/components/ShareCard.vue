<template>
    <article class="share-card" :class="{ clickable }" @click="handleOpen">
        <header class="sc-head">
            <div class="sc-avatar" :style="{ background: avatarColor }">{{ avatarText }}</div>
            <div class="sc-author">
                <div class="sc-name">{{ authorName }}</div>
                <div class="sc-time">{{ timeText }}</div>
            </div>
            <span v-if="share.interestName" class="sc-interest" :style="interestStyle">
                # {{ share.interestName }}
            </span>
        </header>

        <h3 class="sc-title">{{ share.title }}</h3>
        <p class="sc-excerpt">{{ excerpt }}</p>

        <div v-if="share.images && share.images.length" class="sc-images">
            <el-image
                v-for="(image, index) in share.images.slice(0, 3)"
                :key="index"
                :src="image"
                fit="cover"
                class="sc-image"
                preview-teleported
                :preview-src-list="share.images"
                :initial-index="index"
                @click.stop
            />
        </div>

        <div v-if="share.ticket" class="sc-ticket" @click.stop="openTicket">
            <span class="sc-ticket-icon">🎫</span>
            <span class="sc-ticket-title">{{ share.ticket.title }}</span>
            <span class="sc-ticket-meta">{{ share.ticket.type || '体验' }}</span>
            <span class="sc-ticket-arrow">↗</span>
        </div>

        <footer class="sc-foot">
            <div class="sc-rating">
                <el-rate :model-value="Number(share.rating) || 0" disabled size="small" />
                <span class="sc-score">{{ scoreText }}</span>
            </div>

            <div class="sc-actions">
                <button
                    type="button"
                    class="sc-action"
                    :class="{ active: share.liked }"
                    :title="share.liked ? '取消点赞' : '点赞'"
                    @click.stop="$emit('like', share)"
                >
                    <span class="sc-heart">{{ share.liked ? '♥' : '♡' }}</span>{{ share.likeCount || 0 }}
                </button>
                <span class="sc-action static">💬 {{ share.commentCount || 0 }}</span>
                <span v-if="share.favoriteCount" class="sc-action static">🔖 {{ share.favoriteCount }}</span>
            </div>
        </footer>
    </article>
</template>

<script setup>
    import { computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { formatRelativeTime, toExcerpt } from '../utils/format'

    const props = defineProps({
    share: {
    type: Object,
    required: true
    },
    clickable: {
    type: Boolean,
    default: true
    }
    })

    defineEmits(['like'])

    const router = useRouter()

    const AVATAR_COLORS = ['#6c5ce7', '#00b894', '#e17055', '#0984e3', '#e84393', '#f39c12']

    const authorName = computed(() => props.share.author?.nickname || '匿名用户')

    const avatarText = computed(() => authorName.value.slice(0, 1))

    const avatarColor = computed(() => {
    if (props.share.author?.color) return props.share.author.color
    let hash = 0
    for (const char of authorName.value) {
    hash = (hash * 31 + char.charCodeAt(0)) % 997
    }
    return AVATAR_COLORS[hash % AVATAR_COLORS.length]
    })

    const timeText = computed(() => formatRelativeTime(props.share.createTime))

    const excerpt = computed(() => toExcerpt(props.share.content, 110))

    const scoreText = computed(() => {
    const rating = Number(props.share.rating) || 0
    return rating ? rating.toFixed(1) : '未评分'
    })

    const interestStyle = computed(() => {
    const hue = ((Number(props.share.interestId) || 1) * 47) % 360
    return {
    color: `hsl(${hue}, 55%, 38%)`,
    background: `hsl(${hue}, 85%, 95%)`
    }
    })

    const handleOpen = () => {
    if (!props.clickable || !props.share.id) return
    router.push(`/share/${props.share.id}`)
    }

    const openTicket = () => {
    if (props.share.ticket?.id) {
    router.push(`/ticket/${props.share.ticket.id}`)
    }
    }
</script>

<style scoped>
    .share-card {
        padding: 20px 22px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 14px;
        transition: box-shadow 0.22s, transform 0.22s, border-color 0.22s;
    }

    .share-card.clickable {
        cursor: pointer;
    }

    .share-card.clickable:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(64, 158, 255, 0.12);
        border-color: #d9ecff;
    }

    .sc-head {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .sc-avatar {
        flex-shrink: 0;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-size: 16px;
        font-weight: 600;
        border-radius: 50%;
    }

    .sc-author {
        flex: 1;
        min-width: 0;
    }

    .sc-name {
        font-size: 14px;
        font-weight: 600;
        color: #303133;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .sc-time {
        font-size: 12px;
        color: #a8abb2;
    }

    .sc-interest {
        flex-shrink: 0;
        padding: 2px 10px;
        font-size: 12px;
        border-radius: 10px;
        white-space: nowrap;
    }

    .sc-title {
        margin: 14px 0 8px;
        font-size: 17px;
        font-weight: 600;
        line-height: 1.5;
        color: #1f2d3d;
    }

    .sc-excerpt {
        display: -webkit-box;
        margin: 0;
        overflow: hidden;
        font-size: 14px;
        line-height: 1.75;
        color: #606266;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }

    .sc-images {
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }

    .sc-image {
        width: 92px;
        height: 92px;
        border-radius: 8px;
        cursor: zoom-in;
    }

    .sc-ticket {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        max-width: 100%;
        margin-top: 12px;
        padding: 6px 12px;
        font-size: 13px;
        color: #606266;
        background: #f7f9fc;
        border: 1px dashed #dcdfe6;
        border-radius: 8px;
        transition: background 0.2s;
    }

    .sc-ticket:hover {
        background: #ecf5ff;
    }

    .sc-ticket-title {
        max-width: 260px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-weight: 600;
        color: #409eff;
    }

    .sc-ticket-meta {
        padding: 1px 7px;
        font-size: 12px;
        color: #909399;
        background: #fff;
        border-radius: 8px;
    }

    .sc-ticket-arrow {
        color: #a8abb2;
    }

    .sc-foot {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px solid #f2f3f5;
    }

    .sc-rating {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .sc-score {
        font-size: 13px;
        font-weight: 600;
        color: #f39c12;
    }

    .sc-actions {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .sc-action {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 4px;
        font-family: inherit;
        font-size: 13px;
        color: #909399;
        background: none;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        transition: color 0.2s, background 0.2s;
    }

    .sc-action:hover {
        color: #f56c6c;
        background: #fef0f0;
    }

    .sc-action.static {
        cursor: default;
    }

    .sc-action.static:hover {
        color: #909399;
        background: none;
    }

    .sc-action.active {
        color: #f56c6c;
    }

    .sc-heart {
        font-size: 15px;
        line-height: 1;
    }

    @media (max-width: 600px) {
        .share-card {
            padding: 16px;
        }

        .sc-title {
            font-size: 16px;
        }

        .sc-actions {
            gap: 10px;
        }
    }
</style>
