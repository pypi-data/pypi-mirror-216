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
        <UNewCalendar
          ref="departureDatetime"
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
        <UNewCalendar
          ref="arrivalDatetime"
          v-model="missionFormModel.legs[legIndex].arrival_datetime"
          :is-validation-dirty="isValidationDirty"
          :min-date="missionFormModel.legs[legIndex].departure_datetime"
          :errors="errors?.arrival_datetime"
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
          <UCheckboxWrapper
            v-model="passengersCheckbox"
            label-text="Passengers?"
            @update:model-value="passengersCheckbox = $event"
          />
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
import { computed, nextTick, PropType, ref } from 'vue'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import { ErrorObject } from '@vuelidate/core'
import ULabel from '@/components/ui/form/ULabel.vue'
import AirportLocationAutocomplete from '@/components/autocomplete/AirportLocationAutocomplete.vue'
import UNewCalendar from '@/components/ui/form/UNewCalendar.vue'
import { getMissionId } from '@/helpers'

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
const departureDatetime = ref()
const arrivalDatetime = ref()

const missionFormStore = useMissionFormStore()
const { formModel: missionFormModel } = storeToRefs(missionFormStore)

const computedMinimumDepartureDate = computed(() => {
  return props.legIndex === 0
    ? null
    : missionFormModel.value?.legs?.[props.legIndex - 1].arrival_datetime
})

const passengersCheckbox = ref(false)

const passengersCheckboxComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex].pob_pax,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) leg.pob_pax = 0
    leg.pob_pax = value
  }
})
const cargoCheckbox = ref(false)

const cargoCheckboxComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex].cob_lbs,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) leg.cob_lbs = 0
    leg.cob_lbs = value
  }
})
const onChangeArrivalLocation = (airportId: number) => {
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]
  if (nextLeg) {
    nextLeg.departure_location = airportId
  }
}
const onChangeDepartureLocation = (airportId: number) => {
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  if (prevLeg && prevLeg.arrival_location !== airportId) {
    prevLeg.arrival_location = airportId
  }
}
const onChangeDepartureTime = async (event) => {
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  await nextTick()
  if (event && !getMissionId()) {
    currentLeg.arrival_datetime = new Date(event)
  }
}
</script>

<style lang="scss" module>
.mission-leg-wrapper {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem];

  &__content {
    @apply grid px-6 gap-x-[1.5rem] gap-y-[2.5px] mt-4  grid-cols-1 sm:grid-cols-2 font-medium text-[1.25rem] text-grey-900;
  }
}
</style>
