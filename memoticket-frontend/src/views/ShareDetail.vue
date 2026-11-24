<template>
    <CommunityPage active="feed">
        <div class="detail-layout">
            <main class="detail-main">
                <router-link to="/community/feed" class="back-link">← 返回社区动态</router-link>

                <!-- 加载中 -->
                <div v-if="loading" class="skeleton-box">
                    <el-skeleton :rows="8" animated />
                </div>

                <template v-else-if="share">
                    <article class="article-card">
                        <header class="article-head">
                            <div class="author-avatar" :style="{ background: avatarColor }">{{ avatarText }}</div>
                            <div class="author-info">
                                <div class="author-name">{{ authorName }}</div>
                                <div class="author-time">{{ formatDateTime(share.createTime) }}</div>
                            </div>
                            <span v-if="share.interestName" class="interest-chip" :style="interestStyle">
                                # {{ share.interestName }}
                            </span>
                        </header>

                        <h1 class="article-title">{{ share.title }}</h1>

                        <div class="article-meta">
                            <span class="meta-item">
                                <el-rate :model-value="Number(share.rating) || 0" disabled size="small" />
                                <strong>{{ Number(share.rating || 0).toFixed(1) }}</strong>
                            </span>
                            <span class="meta-dot">·</span>
                            <span class="meta-item">👍 {{ share.likeCount || 0 }} 赞</span>
                            <span class="meta-dot">·</span>
                            <span class="meta-item">💬 {{ share.commentCount || 0 }} 评论</span>
                        </div>

                        <div class="article-body">
                            <p v-for="(paragraph, index) in paragraphs" :key="index">{{ paragraph }}</p>
                        </div>

                        <div v-if="share.images && share.images.length" class="article-images">
                            <el-image
                                v-for="(image, index) in share.images"
                                :key="index"
                                :src="image"
                                fit="cover"
                                class="article-image"
                                preview-teleported
                                :preview-src-list="share.images"
                                :initial-index="index"
                            />
                        </div>

                        <div v-if="share.tags && share.tags.length" class="article-tags">
                            <span v-for="tag in share.tags" :key="tag" class="tag-item">#{{ tag }}</span>
                        </div>

                        <div v-if="share.ticket" class="linked-ticket" @click="openTicket">
                            <span class="linked-icon">🎫</span>
                            <div class="linked-body">
                                <div class="linked-title">{{ share.ticket.title }}</div>
                                <div class="linked-meta">
                                    {{ share.ticket.type || '体验' }}
                                    <template v-if="share.ticket.venue"> · {{ share.ticket.venue }}</template>
                                    <template v-if="share.ticket.eventDate"> · {{ share.ticket.eventDate }}</template>
                                </div>
                            </div>
                            <span class="linked-arrow">查看票根 →</span>
                        </div>

                        <footer class="article-actions">
                            <button type="button" class="action-btn like" :class="{ active: share.liked }" @click="handleLike">
                                <span class="action-icon">{{ share.liked ? '♥' : '♡' }}</span>
                                {{ share.liked ? '已赞' : '点赞' }} {{ share.likeCount || 0 }}
                            </button>
                            <button
                                type="button"
                                class="action-btn favorite"
                                :class="{ active: share.favorited }"
                                @click="handleFavorite"
                            >
                                <span class="action-icon">🔖</span>
                                {{ share.favorited ? '已收藏' : '收藏' }} {{ share.favoriteCount || 0 }}
                            </button>
                            <button type="button" class="action-btn" @click="scrollToComments">
                                <span class="action-icon">💬</span> 评论 {{ share.commentCount || 0 }}
                            </button>
                            <button type="button" class="action-btn" @click="copyLink">
                                <span class="action-icon">🔗</span> 复制链接
                            </button>
                        </footer>
                    </article>

                    <!-- 评论 -->
                    <section ref="commentsRef" class="comments-card">
                        <div class="comments-head">
                            <h2>评论 <span>{{ share.commentCount || 0 }}</span></h2>
                        </div>

                        <div v-if="isLoggedIn" class="comment-editor">
                            <el-input
                                v-model="commentDraft"
                                type="textarea"
                                :rows="3"
                                maxlength="300"
                                show-word-limit
                                placeholder="友善讨论，说说你的看法…"
                            />
                            <div class="comment-editor-actions">
                                <el-button
                                    type="primary"
                                    :loading="commentSubmitting"
                                    :disabled="!commentDraft.trim()"
                                    @click="submitComment"
                                >
                                    发表评论
                                </el-button>
                            </div>
                        </div>

                        <div v-else class="login-tip">
                            <span>登录后可以点赞、收藏和参与讨论</span>
                            <el-button type="primary" plain size="small" @click="goLogin">去登录</el-button>
                        </div>

                        <div v-if="commentsLoading" class="comment-loading">
                            <el-skeleton :rows="3" animated />
                        </div>

                        <div v-else-if="comments.length" class="comment-list">
                            <div v-for="comment in comments" :key="comment.id" class="comment-item">
                                <div class="comment-avatar" :style="{ background: commentColor(comment) }">
                                    {{ (comment.author?.nickname || '匿').slice(0, 1) }}
                                </div>
                                <div class="comment-body">
                                    <div class="comment-head">
                                        <span class="comment-name">{{ comment.author?.nickname || '匿名用户' }}</span>
                                        <span class="comment-time">{{ formatRelativeTime(comment.createTime) }}</span>
                                    </div>
                                    <p class="comment-content">{{ comment.content }}</p>
                                </div>
                            </div>
                        </div>

                        <el-empty v-else description="还没有评论，来说说你的看法" :image-size="70" />
                    </section>
                </template>

                <div v-else class="empty-box">
                    <el-empty description="这篇分享不存在，可能已被删除">
                        <el-button type="primary" @click="router.push('/community/feed')">回到社区动态</el-button>
                    </el-empty>
                </div>
            </main>

            <aside v-if="share" class="detail-side">
                <div class="side-card">
                    <h3>关于作者</h3>
                    <div class="side-author">
                        <div class="author-avatar small" :style="{ background: avatarColor }">{{ avatarText }}</div>
                        <div>
                            <div class="author-name">{{ authorName }}</div>
                            <div class="author-time">感谢 TA 的真实分享</div>
                        </div>
                    </div>
                </div>

                <div class="side-card cta-card">
                    <h3>你也体验过？</h3>
                    <p>把这次的感受写下来，顺便关联你的票根。</p>
                    <el-button type="primary" style="width: 100%" @click="router.push('/share/create')">
                        ✏️ 发布我的分享
                    </el-button>
                </div>

                <div v-if="share.interestName" class="side-card">
                    <h3>同好聚集地</h3>
                    <p>在「{{ share.interestName }}」里还有更多相似的体验。</p>
                    <el-button
                        link
                        type="primary"
                        @click="router.push(`/community/feed?interest=${share.interestId}`)"
                    >
                        浏览该兴趣的动态 →
                    </el-button>
                </div>
            </aside>
        </div>
    </CommunityPage>
</template>

<script setup>
    import { computed, nextTick, onMounted, ref, watch } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import CommunityPage from '../components/CommunityPage.vue'
    import { formatDateTime, formatRelativeTime } from '../utils/format'
    import {
        createCommentApi,
        getCommentListApi,
        getShareDetailApi,
        toggleShareFavoriteApi,
        toggleShareLikeApi
    } from '../api/community'

    const route = useRoute()
    const router = useRouter()

    const loading = ref(false)
    const share = ref(null)
    const comments = ref([])
    const commentsLoading = ref(false)
    const commentDraft = ref('')
    const commentSubmitting = ref(false)
    const commentsRef = ref(null)
    const isLoggedIn = ref(Boolean(localStorage.getItem('token')))

    const AVATAR_COLORS = ['#6c5ce7', '#00b894', '#e17055', '#0984e3', '#e84393', '#f39c12']

    const authorName = computed(() => share.value?.author?.nickname || '匿名用户')
    const avatarText = computed(() => authorName.value.slice(0, 1))

    const avatarColor = computed(() => {
    if (share.value?.author?.color) return share.value.author.color
    let hash = 0
    for (const char of authorName.value) {
    hash = (hash * 31 + char.charCodeAt(0)) % 997
    }
    return AVATAR_COLORS[hash % AVATAR_COLORS.length]
    })

    const interestStyle = computed(() => {
    const hue = ((Number(share.value?.interestId) || 1) * 47) % 360
    return {
    color: `hsl(${hue}, 55%, 38%)`,
    background: `hsl(${hue}, 85%, 95%)`
    }
    })

    const paragraphs = computed(() =>
    String(share.value?.content || '')
      .split(/\n+/)
      .map((item) => item.trim())
      .filter(Boolean)
    )

    const commentColor = (comment) => {
    if (comment.author?.color) return comment.author.color
    let hash = 0
    for (const char of comment.author?.nickname || '匿名') {
    hash = (hash * 31 + char.charCodeAt(0)) % 997
    }
    return AVATAR_COLORS[hash % AVATAR_COLORS.length]
    }

    const loadDetail = async () => {
    const id = route.params.id
    loading.value = true
    share.value = null
    comments.value = []
    try {
    const res = await getShareDetailApi(id)
    share.value = res.data || null
    } catch (error) {
    console.error('分享详情加载失败', error)
    share.value = null
    } finally {
    loading.value = false
    }

    if (share.value) {
    loadComments(id)
    }
    }

    const loadComments = async (id) => {
    commentsLoading.value = true
    try {
    const res = await getCommentListApi(id)
    comments.value = res.data || []
    comments.value.sort((a, b) => String(a.createTime).localeCompare(String(b.createTime)))
    } catch (error) {
    console.error('评论加载失败', error)
    comments.value = []
    } finally {
    commentsLoading.value = false
    }
    }

    const requireLogin = () => {
    isLoggedIn.value = Boolean(localStorage.getItem('token'))
    if (isLoggedIn.value) return true
    ElMessage.warning('请先登录')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return false
    }

    const handleLike = async () => {
    if (!requireLogin() || !share.value) return
    try {
    const res = await toggleShareLikeApi(share.value.id)
    if (res.data) {
    share.value.liked = res.data.liked
    share.value.likeCount = res.data.likeCount
    }
    } catch (error) {
    console.error('点赞失败', error)
    }
    }

    const handleFavorite = async () => {
    if (!requireLogin() || !share.value) return
    try {
    const res = await toggleShareFavoriteApi(share.value.id)
    if (res.data) {
    share.value.favorited = res.data.favorited
    share.value.favoriteCount = res.data.favoriteCount
    ElMessage.success(res.data.favorited ? '已收藏' : '已取消收藏')
    }
    } catch (error) {
    console.error('收藏失败', error)
    }
    }

    const submitComment = async () => {
    if (!requireLogin() || !share.value) return
    if (commentSubmitting.value) return

    const content = commentDraft.value.trim()
    if (content.length < 2) {
    ElMessage.warning('评论至少 2 个字')
    return
    }

    commentSubmitting.value = true
    try {
    const res = await createCommentApi(share.value.id, content)
    if (res.data) {
    comments.value.push(res.data)
    share.value.commentCount = (share.value.commentCount || 0) + 1
    commentDraft.value = ''
    ElMessage.success('评论已发布')
    }
    } catch (error) {
    console.error('评论失败', error)
    } finally {
    commentSubmitting.value = false
    }
    }

    const scrollToComments = async () => {
    await nextTick()
    commentsRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }

    const copyLink = async () => {
    const link = window.location.href
    try {
    if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(link)
    } else {
    throw new Error('clipboard unavailable')
    }
    ElMessage.success('链接已复制')
    } catch (error) {
    console.warn('复制失败，请手动复制', error)
    ElMessage.info(`请手动复制链接：${link}`)
    }
    }

    const openTicket = () => {
    if (share.value?.ticket?.id) {
    router.push(`/ticket/${share.value.ticket.id}`)
    }
    }

    const goLogin = () => {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    }

    watch(
    () => route.params.id,
    () => {
    if (route.name === 'ShareDetail') {
    loadDetail()
    }
    }
    )

    onMounted(loadDetail)
</script>

<style scoped>
    .detail-layout {
        display: flex;
        align-items: flex-start;
        gap: 24px;
    }

    .detail-main {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .back-link {
        font-size: 13px;
        color: #909399;
        text-decoration: none;
    }

    .back-link:hover {
        color: #409eff;
    }

    .skeleton-box,
    .empty-box {
        padding: 26px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
    }

    .article-card {
        padding: 32px 34px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
    }

    .article-head {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .author-avatar {
        flex-shrink: 0;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 600;
        color: #fff;
        border-radius: 50%;
    }

    .author-avatar.small {
        width: 36px;
        height: 36px;
        font-size: 15px;
    }

    .author-info {
        flex: 1;
        min-width: 0;
    }

    .author-name {
        font-size: 15px;
        font-weight: 600;
        color: #303133;
    }

    .author-time {
        font-size: 12px;
        color: #a8abb2;
    }

    .interest-chip {
        flex-shrink: 0;
        padding: 3px 12px;
        font-size: 12px;
        border-radius: 11px;
        white-space: nowrap;
    }

    .article-title {
        margin: 20px 0 10px;
        font-size: 27px;
        font-weight: 700;
        line-height: 1.42;
        letter-spacing: 0.3px;
        color: #1f2d3d;
    }

    .article-meta {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #909399;
    }

    .meta-item {
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .meta-item strong {
        color: #f39c12;
    }

    .meta-dot {
        color: #dcdfe6;
    }

    .article-body {
        margin-top: 22px;
        font-size: 15.5px;
        line-height: 1.95;
        color: #4a4f57;
    }

    .article-body p {
        margin: 0 0 16px;
    }

    .article-body p:last-child {
        margin-bottom: 0;
    }

    .article-images {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }

    .article-image {
        width: 190px;
        height: 130px;
        border-radius: 10px;
        cursor: zoom-in;
    }

    .article-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 20px;
    }

    .tag-item {
        padding: 3px 10px;
        font-size: 12px;
        color: #409eff;
        background: #ecf5ff;
        border-radius: 9px;
    }

    .linked-ticket {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 22px;
        padding: 14px 16px;
        background: #f7f9fc;
        border: 1px dashed #dcdfe6;
        border-radius: 12px;
        cursor: pointer;
        transition: background 0.2s, border-color 0.2s;
    }

    .linked-ticket:hover {
        background: #ecf5ff;
        border-color: #b3d8ff;
    }

    .linked-icon {
        font-size: 22px;
    }

    .linked-body {
        flex: 1;
        min-width: 0;
    }

    .linked-title {
        font-size: 14px;
        font-weight: 600;
        color: #303133;
    }

    .linked-meta {
        font-size: 12px;
        color: #909399;
    }

    .linked-arrow {
        flex-shrink: 0;
        font-size: 12px;
        color: #409eff;
    }

    .article-actions {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        margin-top: 26px;
        padding-top: 20px;
        border-top: 1px solid #f2f3f5;
    }

    .action-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 14px;
        font-family: inherit;
        font-size: 13px;
        color: #606266;
        background: #f7f9fc;
        border: 1px solid #ebeef5;
        border-radius: 18px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .action-btn:hover {
        color: #409eff;
        background: #ecf5ff;
        border-color: #d9ecff;
    }

    .action-btn.active.like {
        color: #f56c6c;
        background: #fef0f0;
        border-color: #fde2e2;
    }

    .action-btn.active.favorite {
        color: #f39c12;
        background: #fdf6ec;
        border-color: #faecd8;
    }

    .action-icon {
        font-size: 15px;
        line-height: 1;
    }

    .comments-card {
        padding: 26px 30px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
        scroll-margin-top: 80px;
    }

    .comments-head h2 {
        margin: 0 0 16px;
        font-size: 18px;
        font-weight: 600;
        color: #1f2d3d;
    }

    .comments-head h2 span {
        font-size: 14px;
        color: #a8abb2;
    }

    .comment-editor-actions {
        display: flex;
        justify-content: flex-end;
        margin-top: 10px;
    }

    .login-tip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 14px 16px;
        font-size: 13px;
        color: #909399;
        background: #f7f9fc;
        border-radius: 10px;
    }

    .comment-loading {
        margin-top: 18px;
    }

    .comment-list {
        margin-top: 8px;
    }

    .comment-item {
        display: flex;
        gap: 12px;
        padding: 16px 0;
        border-top: 1px solid #f5f6f8;
    }

    .comment-item:first-child {
        border-top: none;
    }

    .comment-avatar {
        flex-shrink: 0;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 600;
        color: #fff;
        border-radius: 50%;
    }

    .comment-body {
        flex: 1;
        min-width: 0;
    }

    .comment-head {
        display: flex;
        align-items: baseline;
        gap: 10px;
    }

    .comment-name {
        font-size: 13px;
        font-weight: 600;
        color: #303133;
    }

    .comment-time {
        font-size: 12px;
        color: #b1b3b8;
    }

    .comment-content {
        margin: 4px 0 0;
        font-size: 14px;
        line-height: 1.8;
        color: #4a4f57;
        word-break: break-word;
    }

    .detail-side {
        position: sticky;
        top: 84px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 292px;
        flex-shrink: 0;
    }

    .side-card {
        padding: 20px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
    }

    .side-card h3 {
        margin: 0 0 10px;
        font-size: 15px;
        font-weight: 600;
        color: #1f2d3d;
    }

    .side-card p {
        margin: 0 0 12px;
        font-size: 13px;
        line-height: 1.7;
        color: #909399;
    }

    .side-author {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .cta-card {
        background: linear-gradient(160deg, #eef5ff, #ffffff);
        border-color: #d9ecff;
    }

    @media (max-width: 980px) {
        .detail-layout {
            flex-direction: column;
        }

        .detail-side {
            position: static;
            width: 100%;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        }

        .article-card {
            padding: 22px 20px;
        }

        .article-title {
            font-size: 22px;
        }

        .comments-card {
            padding: 20px;
        }

        .article-image {
            width: 100%;
            height: 160px;
        }
    }
</style>
