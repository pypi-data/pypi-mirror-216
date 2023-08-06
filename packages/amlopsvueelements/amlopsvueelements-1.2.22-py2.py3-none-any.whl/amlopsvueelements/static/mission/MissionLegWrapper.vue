<template>
  <div :class="[$style['mission-leg-wrapper']]">
    <div :class="[$style['mission-leg-wrapper__content']]">
      <AirportLocationAutocomplete
        v-model="missionFormModel.legs[legIndex].departure_location"
        :errors="errors?.departure_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Departure Airport:"
        @update:model-value="onChangeDepartureLocation"
      />
      <div class="flex flex-col">
        <ULabel required label-text="Departure Date:" />
        <UCalendar
          v-model="missionFormModel.legs[legIndex].departure_datetime"
          :is-validation-dirty="isValidationDirty"
          :errors="errors?.departure_datetime"
          :min-date="computedMinimumDepartureDate"
          required
          @update:model-value="onChangeDepartureTime"
        />
      </div>
      <AirportLocationAutocomplete
        v-model="missionFormModel.legs[legIndex].arrival_location"
        :errors="errors?.arrival_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Destination Airport:"
        @update:model-value="onChangeArrivalLocation"
      />
      <div class="flex flex-col">
        <ULabel required label-text="Arrival Date:" />
        <UCalendar
          v-model="missionFormModel.legs[legIndex].arrival_datetime"
          :is-validation-dirty="isValidationDirty"
          :errors="errors?.arrival_datetime"
          :min-date="missionFormModel.legs[legIndex].departure_datetime"
          required
          @update:model-value="onChangeDepartureTime"
        />
      </div>
      <UInputWrapper
        v-model="missionFormModel.legs[legIndex].callsign_override"
        :errors="errors?.callsign_override"
        :is-validation-dirty="isValidationDirty"
        label-text="Callsign (if different):"
      />
      <UInputWrapper
        v-model="missionFormModel.legs[legIndex].pob_crew"
        required
        type="number"
        :is-validation-dirty="isValidationDirty"
        label-text="Crew:"
        :errors="errors?.pob_crew"
      />
    </div>
  </div>
  <div class="flex mb-[18px]">
    <div class="flex px-[1.5rem] mt-[6px] gap-[1.5rem] w-full">
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper v-model="passengersCheckbox" label-text="Passengers?" />
          <UInputWrapper
            v-model="passengersCheckboxComputed"
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.pob_pax"
            :disabled="!passengersCheckbox"
          />
        </div>
      </div>
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper v-model="cargoCheckbox" label-text="Cargo?" />
          <UInputWrapper
            v-model="cargoCheckboxComputed"
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.cob_lbs"
            :disabled="!cargoCheckbox"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, nextTick, PropType, ref, watch } from 'vue'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import { ErrorObject } from '@vuelidate/core'
import ULabel from '@/components/ui/form/ULabel.vue'
import AirportLocationAutocomplete from '@/components/autocomplete/AirportLocationAutocomplete.vue'
import { getMissionId } from '@/helpers'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import UCalendar from '@/components/ui/form/UCalendar.vue'

const props = defineProps({
  legIndex: {
    type: Number,
    default: 0
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => {}
  }
})

const missionFormStore = useMissionFormStore()
const missionsReferenceStore = useMissionReferenceStore()
const { selectedDestinationAirportsLeg, airportLocations } = storeToRefs(missionsReferenceStore)
const { formModel: missionFormModel } = storeToRefs(missionFormStore)

const computedMinimumDepartureDate = computed(() => {
  return props.legIndex === 0
    ? missionFormModel.value?.legs?.[props.legIndex].departure_datetime
    : missionFormModel.value?.legs?.[props.legIndex - 1].arrival_datetime
})

const passengersCheckbox = ref(false)

const passengersCheckboxComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.pob_pax,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) leg.pob_pax = 0
    leg.pob_pax = value
  }
})
const cargoCheckbox = ref(false)

const cargoCheckboxComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.cob_lbs,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) leg.cob_lbs = 0
    leg.cob_lbs = value
  }
})
const isLastLeg = computed(() => {
  return props.legIndex === missionFormModel.value?.legs?.length - 1
})
const isFirstLeg = computed(() => {
  return props.legIndex === 0
})
const onChangeDepartureLocation = (airportId: number) => {
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  if (prevLeg && prevLeg.arrival_location !== airportId) {
    prevLeg.arrival_location = airportId
  }
  getMissionId() && !isFirstLeg.value && resetFuelingSection(props.legIndex - 1)
}
const onChangeArrivalLocation = (airport: number) => {
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]
  selectedDestinationAirportsLeg.value[props.legIndex] = airportLocations.value?.find(
    (el: any) => el.id === airport?.id
  )
  if (nextLeg) {
    nextLeg.departure_location = airport
  }
  getMissionId() && !isLastLeg.value && resetFuelingSection(props.legIndex)
}
const onChangeDepartureTime = async (event) => {
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  await nextTick()
  if (event && !getMissionId()) {
    currentLeg.arrival_datetime = new Date(event)
  }
}

const resetFuelingSection = (index) => {
  if (missionFormModel.value.legs[index]) {
    missionFormModel.value.legs[index].arrival_aml_service = false
    delete missionFormModel.value.legs[index].servicing
  }
}
watch(
  () => [cargoCheckboxComputed.value, passengersCheckboxComputed.value],
  ([cargo, passenger]) => {
    cargoCheckbox.value = !!cargo
    passengersCheckbox.value = !!passenger
  },
  { immediate: true }
)
</script>

<style lang="scss" module>
.mission-leg-wrapper {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem];

  &__content {
    @apply grid px-6 gap-x-[1.5rem] gap-y-[2.5px] mt-4  grid-cols-1 sm:grid-cols-2 font-medium text-[1.25rem] text-grey-900;
  }
}
</style>
