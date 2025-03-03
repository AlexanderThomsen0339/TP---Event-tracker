<template>
  <div class="about">
    <h1>This is an about page</h1>
    <EventListTemplate />
  </div>
</template>

<script>
import EventListTemplate from '@/components/EventListTemplate.vue'

export default {
  name: 'AboutView',
  components: {
    EventListTemplate
  }
}
</script>
