<template>
    <CommunityPage active="home">
        <!-- 顶部介绍 -->
        <section class="hero">
            <div class="hero-copy">
                <span class="hero-badge">兴趣社区 · 体验分享</span>
                <h1>把每一次心动<br />写成一张票根</h1>
                <p class="hero-desc">
                    看一场电影、走一段山路、打通一款游戏——把当时的感受留在这里，
                    也看看和你口味相近的人，最近都在体验什么。
                </p>
                <div class="hero-actions">
                    <el-button type="primary" size="large" round @click="goPublish">✏️ 发布我的体验</el-button>
                    <el-button size="large" round @click="goFeed">逛逛社区动态</el-button>
                </div>
                <p class="hero-hint">
                    {{ formatNumber(stats.shareCount) }} 篇体验分享 · {{ formatNumber(stats.authorCount) }} 位分享者 ·
                    {{ formatNumber(stats.commentCount) }} 条讨论
                </p>
            </div>

            <div class="hero-art" aria-hidden="true">
                <div class="ticket-stack">
                    <div class="ticket-card back"></div>
                    <div class="ticket-card mid"></div>
                    <div class="ticket-card front">
                        <div class="tc-top">
                            <span>MEMOTICKET</span>
                            <span>ADMIT ONE</span>
                        </div>
                        <div class="tc-title">《奥本海默》</div>
                        <div class="tc-stars">★★★★★</div>
                        <div class="tc-meta">2026.11.01 · 万达影城 IMAX</div>
                        <div class="tc-rule"></div>
                        <div class="tc-foot">
                            <span>NO. 000128</span>
                            <span>兴趣 · 科幻电影</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 数据概览 -->
        <section class="stats">
            <div v-for="item in statCards" :key="item.label" class="stat-item">
                <strong>{{ loading ? '—' : formatNumber(item.value) }}</strong>
                <span>{{ item.label }}</span>
            </div>
        </section>

        <el-alert
            v-if="errorMessage"
            class="load-error"
            type="warning"
            :closable="false"
            show-icon
            :title="errorMessage"
        >
            <el-button link type="primary" @click="loadOverview">重新加载</el-button>
        </el-alert>

        <div class="home-layout">
            <div class="home-main">
                <!-- 兴趣分类 -->
                <section class="block">
                    <div class="block-head">
                        <div>
                            <h2>兴趣分类</h2>
                            <p>先挑一个你最近在玩、在看、在去的主题。</p>
                        </div>
                        <router-link class="block-more" to="/community/feed">全部动态 →</router-link>
                    </div>

                    <el-skeleton v-if="loading" :rows="3" animated />

                    <div v-else class="interest-grid">
                        <router-link
                            v-for="interest in interests"
                            :key="interest.id"
                            :to="`/community/feed?interest=${interest.id}`"
                            class="interest-card"
                            :style="interestStyle(interest.id)"
                        >
                            <span class="interest-icon">{{ interest.icon || '🌟' }}</span>
                            <span class="interest-name">{{ interest.name }}</span>
                            <span class="interest-count">{{ interest.shareCount || 0 }} 篇分享</span>
                        </router-link>
                    </div>
                </section>

                <!-- 热门分享 -->
                <section class="block">
                    <div class="block-head">
                        <div>
                            <h2>热门体验分享</h2>
                            <p>最近被点赞和讨论最多的体验。</p>
                        </div>
                        <router-link class="block-more" to="/community/feed?sort=hot">更多热帖 →</router-link>
                    </div>

                    <div v-if="loading" class="skeleton-list">
                        <el-skeleton v-for="index in 2" :key="index" :rows="4" animated />
                    </div>

                    <div v-else-if="hotShares.length" class="hot-list">
                        <ShareCard
                            v-for="share in hotShares"
                            :key="share.id"
                            :share="share"
                            @like="handleLike"
                        />
                    </div>

                    <el-empty v-else description="还没有体验分享，来发第一条吧" :image-size="90" />
                </section>
            </div>

            <!-- 侧栏 -->
            <aside class="home-side">
                <div class="side-card publish-card">
                    <h3>有想分享的体验？</h3>
                    <p>关联你的票根，评分、地点和日期会自动带进分享内容。</p>
                    <el-button type="primary" style="width: 100%" @click="goPublish">开始写分享</el-button>
                </div>

                <div class="side-card">
                    <h3>社区公约</h3>
                    <ul class="rule-list">
                        <li>真诚记录，比“好看”更重要</li>
                        <li>标题别剧透，把惊喜留给别人</li>
                        <li>口味不同很正常，友善讨论</li>
                        <li>不放广告和外链</li>
                    </ul>
                </div>

                <div class="side-card">
                    <h3>快捷入口</h3>
                    <div class="quick-links">
                        <router-link to="/community/feed">社区动态</router-link>
                        <router-link to="/share/create">发布分享</router-link>
                        <router-link to="/tickets">我的票夹</router-link>
                        <router-link to="/profile">个人主页</router-link>
                    </div>
                </div>
            </aside>
        </div>
    </CommunityPage>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import CommunityPage from '../components/CommunityPage.vue'
    import ShareCard from '../components/ShareCard.vue'
    import {
        getCommunityOverviewApi,
        toggleShareLikeApi,
        COMMUNITY_DEMO_MODE
    } from '../api/community'

    const router = useRouter()

    const loading = ref(false)
    const errorMessage = ref('')
    const stats = ref({
    shareCount: 0,
    interestCount: 0,
    authorCount: 0,
    commentCount: 0
    })
    const interests = ref([])
    const hotShares = ref([])

    const statCards = computed(() => [
    { label: '体验分享', value: stats.value.shareCount },
    { label: '兴趣分类', value: stats.value.interestCount },
    { label: '分享者', value: stats.value.authorCount },
    { label: '条讨论', value: stats.value.commentCount }
    ])

    const formatNumber = (value) => Number(value || 0).toLocaleString('zh-CN')

    const interestStyle = (id) => {
    const hue = ((Number(id) || 1) * 47) % 360
    return {
    background: `linear-gradient(135deg, hsl(${hue}, 90%, 97%), #ffffff)`,
    borderColor: `hsl(${hue}, 80%, 88%)`
    }
    }

    const loadOverview = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
    const res = await getCommunityOverviewApi()
    const data = res.data || {}
    stats.value = { ...stats.value, ...(data.stats || {}) }
    interests.value = data.interests || []
    hotShares.value = data.hot || []
    } catch (error) {
    console.error('社区首页数据加载失败', error)
    errorMessage.value = COMMUNITY_DEMO_MODE
      ? '社区首页数据加载失败，请稍后重试。'
      : '社区首页数据加载失败，请确认后端服务是否已启动。'
    } finally {
    loading.value = false
    }
    }

    const handleLike = async (share) => {
    if (!localStorage.getItem('token')) {
    ElMessage.warning('登录后才能点赞哦')
    router.push({ path: '/login', query: { redirect: '/community' } })
    return
    }

    try {
    const res = await toggleShareLikeApi(share.id)
    const updated = res.data
    if (!updated) return
    const target = hotShares.value.find((item) => item.id === updated.id)
    if (target) {
    target.liked = updated.liked
    target.likeCount = updated.likeCount
    }
    } catch (error) {
    console.error('点赞失败', error)
    }
    }

    const goPublish = () => router.push('/share/create')
    const goFeed = () => router.push('/community/feed')

    onMounted(loadOverview)
</script>

<style scoped>
    .hero {
        display: flex;
        align-items: center;
        gap: 32px;
        padding: 40px 40px 36px;
        background: linear-gradient(135deg, #eef4ff 0%, #f7f2ff 55%, #fff 100%);
        border: 1px solid #e6ecf9;
        border-radius: 20px;
    }

    .hero-copy {
        flex: 1;
        min-width: 0;
    }

    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        margin-bottom: 14px;
        font-size: 12px;
        color: #409eff;
        background: #fff;
        border: 1px solid #d9ecff;
        border-radius: 12px;
    }

    .hero h1 {
        margin: 0 0 14px;
        font-size: 38px;
        font-weight: 700;
        line-height: 1.28;
        letter-spacing: 0.5px;
        color: #1f2d3d;
    }

    .hero-desc {
        max-width: 460px;
        margin: 0 0 22px;
        font-size: 15px;
        line-height: 1.8;
        color: #606266;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
    }

    .hero-actions :deep(.el-button) {
        margin-left: 0;
    }

    .hero-hint {
        margin: 18px 0 0;
        font-size: 13px;
        color: #909399;
    }

    .hero-art {
        flex-shrink: 0;
        width: 300px;
        display: flex;
        justify-content: center;
    }

    .ticket-stack {
        position: relative;
        width: 260px;
        height: 168px;
    }

    .ticket-card {
        position: absolute;
        inset: 0;
        border-radius: 14px;
    }

    .ticket-card.back {
        background: linear-gradient(135deg, #a8c8ff, #c4b5fd);
        transform: rotate(-8deg) translate(-10px, 6px);
        opacity: 0.55;
    }

    .ticket-card.mid {
        background: linear-gradient(135deg, #dbeafe, #ede9fe);
        transform: rotate(-3deg) translate(-3px, 3px);
        opacity: 0.9;
    }

    .ticket-card.front {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 18px 20px;
        background: #fff;
        border: 1px solid #e4e8f0;
        box-shadow: 0 16px 32px rgba(64, 158, 255, 0.16);
        transform: rotate(2deg);
    }

    .tc-top {
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        letter-spacing: 1.2px;
        color: #a8abb2;
    }

    .tc-title {
        margin-top: 6px;
        font-size: 22px;
        font-weight: 700;
        color: #1f2d3d;
    }

    .tc-stars {
        margin-top: 2px;
        font-size: 14px;
        letter-spacing: 3px;
        color: #f39c12;
    }

    .tc-meta {
        margin-top: 4px;
        font-size: 12px;
        color: #909399;
    }

    .tc-rule {
        margin: 8px 0;
        border-top: 1px dashed #dcdfe6;
    }

    .tc-foot {
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        color: #b1b3b8;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin: 18px 0 26px;
    }

    .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        padding: 14px 10px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 12px;
    }

    .stat-item strong {
        font-size: 22px;
        font-weight: 700;
        color: #1f2d3d;
    }

    .stat-item span {
        font-size: 12px;
        color: #909399;
    }

    .load-error {
        margin-bottom: 18px;
    }

    .home-layout {
        display: flex;
        align-items: flex-start;
        gap: 24px;
    }

    .home-main {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 26px;
    }

    .block {
        padding: 24px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
    }

    .block-head {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 18px;
    }

    .block-head h2 {
        margin: 0;
        font-size: 19px;
        font-weight: 600;
        color: #1f2d3d;
    }

    .block-head p {
        margin: 4px 0 0;
        font-size: 13px;
        color: #909399;
    }

    .block-more {
        flex-shrink: 0;
        font-size: 13px;
        color: #409eff;
        text-decoration: none;
    }

    .block-more:hover {
        text-decoration: underline;
    }

    .interest-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }

    .interest-card {
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding: 14px 14px 12px;
        text-decoration: none;
        border: 1px solid #ebeef5;
        border-radius: 12px;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .interest-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(31, 45, 61, 0.08);
    }

    .interest-icon {
        font-size: 20px;
    }

    .interest-name {
        margin-top: 2px;
        font-size: 14px;
        font-weight: 600;
        color: #303133;
    }

    .interest-count {
        font-size: 12px;
        color: #909399;
    }

    .hot-list,
    .skeleton-list {
        display: flex;
        flex-direction: column;
        gap: 14px;
    }

    .home-side {
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 288px;
        flex-shrink: 0;
    }

    .side-card {
        padding: 20px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
    }

    .side-card h3 {
        margin: 0 0 8px;
        font-size: 15px;
        font-weight: 600;
        color: #1f2d3d;
    }

    .side-card p {
        margin: 0 0 14px;
        font-size: 13px;
        line-height: 1.7;
        color: #909399;
    }

    .publish-card {
        background: linear-gradient(160deg, #eef5ff, #fff);
        border-color: #d9ecff;
    }

    .rule-list {
        margin: 0;
        padding-left: 16px;
        font-size: 13px;
        line-height: 2;
        color: #606266;
    }

    .quick-links {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .quick-links a {
        padding: 8px 10px;
        font-size: 13px;
        text-align: center;
        color: #606266;
        text-decoration: none;
        background: #f7f9fc;
        border-radius: 8px;
        transition: color 0.2s, background 0.2s;
    }

    .quick-links a:hover {
        color: #409eff;
        background: #ecf5ff;
    }

    @media (max-width: 1000px) {
        .hero {
            flex-direction: column;
            align-items: flex-start;
            padding: 28px 24px;
        }

        .hero-art {
            width: 100%;
            justify-content: flex-start;
        }

        .home-layout {
            flex-direction: column;
        }

        .home-side {
            width: 100%;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        }
    }

    @media (max-width: 680px) {
        .hero h1 {
            font-size: 28px;
        }

        .interest-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .stats {
            grid-template-columns: repeat(2, 1fr);
        }

        .block {
            padding: 18px 16px;
        }

        .ticket-stack {
            width: 100%;
            max-width: 280px;
        }
    }
</style>
