<template>
    <CommunityPage active="feed">
        <div class="page-head">
            <div class="page-head-main">
                <router-link to="/community" class="back-link">← 返回社区首页</router-link>
                <h1>社区动态</h1>
                <p>看看大家最近看了什么、玩了什么、去了哪里。</p>
            </div>
            <el-button type="primary" round size="large" @click="goPublish">✏️ 发布体验</el-button>
        </div>

        <!-- 筛选栏 -->
        <div class="filter-bar">
            <el-input
                v-model="keywordInput"
                class="filter-search"
                placeholder="搜索标题、内容或标签"
                clearable
                @keyup.enter="applyKeyword"
                @clear="applyKeyword"
            >
                <template #append>
                    <el-button @click="applyKeyword">搜索</el-button>
                </template>
            </el-input>

            <el-select
                v-model="filters.interestId"
                class="filter-interest"
                placeholder="全部兴趣"
                clearable
                @change="handleFilterChange"
            >
                <el-option
                    v-for="interest in interests"
                    :key="interest.id"
                    :label="interest.name"
                    :value="interest.id"
                />
            </el-select>

            <el-radio-group v-model="filters.sort" class="filter-sort" @change="handleFilterChange">
                <el-radio-button value="latest">最新</el-radio-button>
                <el-radio-button value="hot">最热</el-radio-button>
            </el-radio-group>

            <el-button v-if="hasFilter" link type="primary" @click="resetFilters">重置</el-button>
        </div>

        <div class="result-meta">
            <span v-if="!loading">
                共 <strong>{{ total }}</strong> 条动态
                <template v-if="activeInterestName"> · 兴趣「{{ activeInterestName }}」</template>
                <template v-if="filters.keyword"> · 关键词「{{ filters.keyword }}」</template>
            </span>
            <span v-else>正在加载动态…</span>
            <router-link class="hot-link" to="/community/feed?sort=hot">🔥 看看最热的帖子</router-link>
        </div>

        <el-alert
            v-if="errorMessage"
            type="warning"
            :closable="false"
            show-icon
            :title="errorMessage"
            class="load-error"
        >
            <el-button link type="primary" @click="fetchFeed">重新加载</el-button>
        </el-alert>

        <!-- 列表 -->
        <div v-if="loading" class="feed-list">
            <div v-for="index in 3" :key="index" class="skeleton-card">
                <el-skeleton :rows="4" animated />
            </div>
        </div>

        <div v-else-if="list.length" class="feed-list">
            <ShareCard v-for="share in list" :key="share.id" :share="share" @like="handleLike" />
        </div>

        <div v-else-if="!errorMessage" class="empty-box">
            <el-empty :description="hasFilter ? '没有找到符合条件的动态，试试换个关键词' : '还没有动态，来发布第一条体验分享吧'">
                <el-button v-if="hasFilter" @click="resetFilters">清除筛选</el-button>
                <el-button v-else type="primary" @click="goPublish">去发布</el-button>
            </el-empty>
        </div>

        <div v-if="total > pageSize" class="pager">
            <el-pagination
                background
                layout="prev, pager, next"
                :total="total"
                :page-size="pageSize"
                :current-page="page"
                @current-change="handlePageChange"
            />
        </div>
    </CommunityPage>
</template>

<script setup>
    import { computed, onMounted, reactive, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import CommunityPage from '../components/CommunityPage.vue'
    import ShareCard from '../components/ShareCard.vue'
    import {
        getCommunityInterestsApi,
        getFeedListApi,
        toggleShareLikeApi
    } from '../api/community'

    const route = useRoute()
    const router = useRouter()

    const interests = ref([])
    const list = ref([])
    const total = ref(0)
    const page = ref(1)
    const pageSize = 5
    const loading = ref(false)
    const errorMessage = ref('')

    const filters = reactive({
    interestId: '',
    sort: 'latest',
    keyword: ''
    })

    const keywordInput = ref('')

    const hasFilter = computed(
    () => Boolean(filters.interestId) || Boolean(filters.keyword) || filters.sort !== 'latest'
    )

    const activeInterestName = computed(() => {
    const target = interests.value.find((item) => item.id === Number(filters.interestId))
    return target ? target.name : ''
    })

    const syncQuery = () => {
    const query = {}
    if (filters.interestId) query.interest = String(filters.interestId)
    if (filters.sort !== 'latest') query.sort = filters.sort
    if (filters.keyword) query.keyword = filters.keyword
    router.replace({ path: '/community/feed', query })
    }

    const fetchFeed = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
    const res = await getFeedListApi({
    interestId: filters.interestId || '',
    sort: filters.sort,
    keyword: filters.keyword,
    page: page.value,
    pageSize
    })
    const data = res.data || {}
    list.value = data.list || []
    total.value = data.total || 0
    } catch (error) {
    console.error('动态列表加载失败', error)
    errorMessage.value = '动态列表加载失败，请检查后端服务后重试。'
    list.value = []
    total.value = 0
    } finally {
    loading.value = false
    }
    }

    const loadInterests = async () => {
    try {
    const res = await getCommunityInterestsApi()
    interests.value = res.data || []
    } catch (error) {
    console.error('兴趣分类加载失败', error)
    }
    }

    const handleFilterChange = () => {
    page.value = 1
    syncQuery()
    fetchFeed()
    }

    const applyKeyword = () => {
    filters.keyword = String(keywordInput.value || '').trim()
    handleFilterChange()
    }

    const resetFilters = () => {
    filters.interestId = ''
    filters.sort = 'latest'
    filters.keyword = ''
    keywordInput.value = ''
    handleFilterChange()
    }

    const handlePageChange = (nextPage) => {
    page.value = nextPage
    fetchFeed()
    window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const handleLike = async (share) => {
    if (!localStorage.getItem('token')) {
    ElMessage.warning('登录后才能点赞哦')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
    }

    try {
    const res = await toggleShareLikeApi(share.id)
    const updated = res.data
    if (!updated) return
    const target = list.value.find((item) => item.id === updated.id)
    if (target) {
    target.liked = updated.liked
    target.likeCount = updated.likeCount
    }
    } catch (error) {
    console.error('点赞失败', error)
    }
    }

    const goPublish = () => router.push('/share/create')

    onMounted(async () => {
    // 支持从首页兴趣卡片带参进入：/community/feed?interest=4&sort=hot
    filters.interestId = route.query.interest ? Number(route.query.interest) : ''
    filters.sort = route.query.sort === 'hot' ? 'hot' : 'latest'
    filters.keyword = String(route.query.keyword || '')
    keywordInput.value = filters.keyword

    await loadInterests()
    await fetchFeed()
    })
</script>

<style scoped>
    .page-head {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 20px;
    }

    .back-link {
        font-size: 13px;
        color: #909399;
        text-decoration: none;
    }

    .back-link:hover {
        color: #409eff;
    }

    .page-head h1 {
        margin: 6px 0 4px;
        font-size: 30px;
        font-weight: 700;
        color: #1f2d3d;
    }

    .page-head p {
        margin: 0;
        font-size: 14px;
        color: #909399;
    }

    .filter-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 14px;
    }

    .filter-search {
        width: 300px;
    }

    .filter-interest {
        width: 168px;
    }

    .filter-sort :deep(.el-radio-button__inner) {
        padding: 8px 18px;
    }

    .result-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 16px 2px 12px;
        font-size: 13px;
        color: #909399;
    }

    .result-meta strong {
        color: #409eff;
    }

    .hot-link {
        color: #909399;
        text-decoration: none;
    }

    .hot-link:hover {
        color: #f39c12;
    }

    .load-error {
        margin-bottom: 14px;
    }

    .feed-list {
        display: flex;
        flex-direction: column;
        gap: 14px;
    }

    .skeleton-card {
        padding: 22px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 14px;
    }

    .empty-box {
        padding: 26px 0;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 14px;
    }

    .pager {
        display: flex;
        justify-content: center;
        margin-top: 22px;
    }

    @media (max-width: 720px) {
        .page-head {
            flex-direction: column;
            align-items: flex-start;
        }

        .page-head h1 {
            font-size: 24px;
        }

        .filter-search {
            width: 100%;
        }

        .filter-interest {
            flex: 1;
            width: auto;
        }

        .result-meta {
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
        }
    }
</style>
