<template>
  <div :class="$style['mission-itinerary']">
    <div :class="$style['mission-itinerary__items']">
      <div
        v-for="(leg, index) in formData.legs as IMissionLeg[]"
        :key="index"
        :class="$style['mission-itinerary__item']"
      >
        <UFormWrapper
          :is-loading="isLoading || isCancelingMissionLeg"
          :class="$style['mission-itinerary__wrapper']"
        >
          <template #header>
            <div :class="$style['mission-itinerary__header']">
              <div :class="$style['mission-itinerary__title']">
                <h1>Mission Leg: {{ leg.sequence_id }}</h1>
              </div>
              <UButton
                v-if="leg.sequence_id !== 1 && formData?.legs?.length >= 3"
                class="bg-transparent p-0"
                :class="$style['mission-itinerary__delete']"
                @click="onDeleteMissionLeg(leg)"
              >
                <img :src="getImageUrl('assets/icons/delete.png')" alt="delete" />
              </UButton>
            </div>
          </template>
          <template #content>
            <MissionLegWrapper
              :is-validation-dirty="validationInfo?.$dirty"
              :leg-index="index"
              :errors="validationInfo?.legs?.$each?.$response?.$errors?.[index] as Record<string, ErrorObject[]>"
            />
          </template>
        </UFormWrapper>
        <div :class="[$style['add-new-mission']]" @click="createMissionLeg(leg.sequence_id)">
          <span :class="$style['add-new-mission__line']" />
          <span :class="$style['add-new-mission__sign']">+</span>
        </div>
      </div>
    </div>
    <div class="my-auto flex flex-col w-1/3 gap-[28px]">
      <template v-for="(leg, index) in formData.legs as IMissionLeg[]" :key="index">
        <div
          v-if="index !== formData.legs?.length - 1"
          class="mission-itinerary__aml"
          :class="$style['mission-itinerary__aml']"
        >
          <div :key="index" :class="$style['mission-itinerary__item']">
            <UFormWrapper
              :form-errors="
                validationInfo?.legs?.$each?.$response?.$errors?.[index]?.arrival_aml_service
              "
              :is-loading="isLoading"
              class="relative"
            >
              <template #content>
                <!--                class="px-[1.5rem] h-[331px] overflow-y-auto"-->

                <AMLTurnaroundWrapper
                  class="px-[1.5rem]"
                  :errors="validationInfo?.legs?.$each?.$response?.$errors?.[index] as Record<string, ErrorObject[]>"
                  :is-validation-dirty="validationInfo?.$dirty"
                  :leg-sequence-id="leg.sequence_id"
                  :leg-index="index"
                  :leg="leg"
                />
              </template>
            </UFormWrapper>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { onBeforeMount, PropType, ref, watch } from 'vue'
import UFormWrapper from '@/components/ui/wrappers/UFormWrapper.vue'
import MissionLegWrapper from '@/components/forms/MissionLegWrapper.vue'
import AMLTurnaroundWrapper from '@/components/forms/AMLTurnaroundWrapper.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import type { IMissionLeg } from '@/types/mission/mission.types'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import { BaseValidation, ErrorObject } from '@vuelidate/core'
import { getImageUrl } from '@/helpers'
import UButton from '@/components/ui/form/UButton.vue'
import { useMission } from '@/composables/mission/useMission'
import { useMissionStore } from '@/stores/useMissionStore'

defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => {}
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  }
})

const missionFormStore = useMissionFormStore()
const missionStore = useMissionStore()
const { createMissionLeg, onDeleteMissionLeg } = useMission()
const { initiateReferenceStore } = useMissionReferenceStore()
const { formModel: formData } = storeToRefs(missionFormStore)
const { isCancelingMissionLeg } = storeToRefs(missionStore)

const marginTop = ref(0)

watch(
  () => formData.value.legs?.[0].servicing?.services?.length,
  (newValue, oldValue) => {
    if (newValue > oldValue) {
      if (marginTop.value < 0) return
      marginTop.value = marginTop.value - 33.5
    } else {
      if (marginTop.value > 251.25) return
      marginTop.value = marginTop.value + 33.5
    }
  },
  { immediate: true }
)

onBeforeMount(async () => {
  await initiateReferenceStore()
})
</script>
<style lang="scss">
.mission-itinerary__aml {
  .ops-form-wrapper__header {
    @apply hidden;
  }
}
</style>
<style lang="scss" module>
.mission-itinerary {
  @apply flex flex-col gap-x-6 w-full sm:flex-row pb-4;
  &__header {
    @apply flex items-center w-full justify-between;
  }
  &__line {
    @apply mx-[1.5rem];
  }
  &__title {
    @apply rounded-md flex items-center;
    img {
      @apply h-4 w-4 mr-1;
      filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(118deg) brightness(107%) contrast(101%);
    }
  }
  &__delete {
    img {
      @apply h-6 w-6;
      filter: invert(23%) sepia(85%) saturate(2552%) hue-rotate(330deg) brightness(87%)
        contrast(103%);
    }
  }
  &__items {
    @apply flex flex-col w-full sm:w-2/3 gap-0;
  }
  &__aml {
    @apply flex flex-col  w-full gap-[1.625rem];
    .ops-form-wrapper__header {
      height: 20px;
      background: red !important;
    }
  }
  &__item {
    .add-new-mission {
      @apply transition-all opacity-0 duration-500 invisible mb-2;
    }
    &:hover {
      .add-new-mission {
        @apply opacity-100 mt-[0.3rem] transition-all duration-500 visible;
      }
    }
  }
  &__wrapper {
    @apply relative;
  }
  .add-new-mission {
    @apply transform duration-500 relative transition-all cursor-pointer z-[1];
    &__line {
      @apply bg-grey-900 absolute top-[53%] h-[1px] w-full block;
    }
    &__sign {
      @apply w-5 h-5 text-grey-800 flex text-[0.96875rem] justify-center rounded-full bg-white mx-auto items-center relative;
    }
  }
}
</style>
