<template>
  <div :class="[$style['ops-aml-turnaround-wrapper']]">
    <div :class="[$style['ops-aml-turnaround__content']]">
      <div class="w-full flex">
        <div @click.stop.prevent.capture="onHandleAmlServicing">
          <UCheckboxWrapper
            :label-text="`AML Servicing at ${arrivalAirportShortName}`"
            :model-value="isAmlServicingEnabled"
            class="!mb-0"
          />
        </div>
      </div>
      <p class="text-center !font-medium !mb-4">
        Fueling
        <span v-if="arrivalAirportShortName">- {{ arrivalAirportShortName }}</span>
      </p>
      <div v-if="missionFormModel.legs[legIndex]?.servicing">
        <div class="flex items-center">
          <p class="text-base whitespace-nowrap min-w-[9rem]">Fuel required:</p>
          <USelectWrapper
            v-model="missionFormModel.legs[legIndex].servicing.fuel_required"
            :disabled="isDisabledField"
            :options="FuelRequiredTypes"
            :reduce="(item) => item.value"
            label="label"
            class="mb-0"
            @update:model-value="onChangeFuellingType"
          />
        </div>
        <div class="flex items-center mt-4">
          <p class="text-base whitespace-nowrap min-w-[9rem]">Quantity:</p>
          <UInputWrapper
            v-model="missionFormModel.legs[legIndex].servicing.fuel_quantity"
            :disabled="isDisabledField || isFuelingDisabled"
            type="number"
            class="!mb-0"
            label="attributes.description"
          />
        </div>
        <div class="flex items-center mt-4">
          <p class="text-base whitespace-nowrap min-w-[9rem]">Unit of Measure:</p>
          <USelectWrapper
            v-model="missionFormModel.legs[legIndex].servicing.fuel_unit"
            :required="!isFuelingDisabled"
            :loading="isLoadingQuantityUnits"
            :options="quantityUnits"
            :errors="errors?.servicing"
            :is-validation-dirty="isValidationDirty"
            :get-option-label="(item) => `${item.description_plural} (${item?.code})`"
            :reduce="(item) => item.id"
            :disabled="isDisabledField || isFuelingDisabled"
            position="top"
            class="!mb-0"
          />
        </div>
        <div class="flex items-center justify-between mt-4">
          <div class="flex items-center">
            <p class="text-base whitespace-nowrap min-w-[9rem]">Prist required?</p>
            <UCheckboxWrapper
              v-model="missionFormModel.legs[legIndex].servicing.fuel_prist_required"
              :disabled="isDisabledField"
              class="mb-0"
            />
          </div>
          <div class="flex">
            <div class="w-full" />
            <div
              v-if="missionFormModel.legs[legIndex].servicing.services?.length"
              class="flex justify-between gap-[0.75rem] text-md items-center"
            >
              <span>Arr</span>
              <span>Dep</span>
            </div>
          </div>
        </div>
        <div class="!mb-4">
          <p class="text-center !font-medium">
            Servicing
            <span v-if="arrivalAirportShortName">- {{ arrivalAirportShortName }}</span>
          </p>
        </div>
        <div class="flex font-medium text-[1.25rem] text-grey-1000">
          <div class="flex flex-col items-center w-full">
            <div class="flex items-start w-full justify-between relative">
              <USelectWrapper
                v-model="missionFormModel.legs[legIndex].servicing.services"
                class="max-w-[310px] w-[76%]"
                placeholder="Select service"
                multiple
                hide-values
                :disabled="isDisabledField"
                :loading="isLoadingServices"
                :options="computedFilteredServiceOptions"
                position="top"
                :get-option-id="(item) => item.id"
                :get-option-label="
                  (item) => {
                    if (item?.attributes) return item?.attributes?.name
                    return serviceOptions?.find((option) => option.id === item.service)?.attributes
                      ?.name
                  }
                "
                :reduce="
                  (item) => {
                    if (!item?.attributes) return item
                    return { service: item?.id, on_arrival: false, on_departure: false }
                  }
                "
                @search="onSearchPrist"
              />
              <div
                v-if="
                  missionFormModel.legs[legIndex].servicing.services?.length && !searchPristQuery
                "
                class="pointer-events-none absolute text-base top-2.5 text-[#a2aeb8] left-4"
              >
                Select service
              </div>
            </div>
            <div
              v-if="missionFormModel.legs[legIndex]?.servicing?.services?.length"
              class="flex w-full justify-between"
            >
              <div class="border border-grey-100 max-w-[310px] w-[76%] rounded-md p-2">
                <div
                  v-for="(service, index) in missionFormModel.legs[legIndex].servicing.services"
                  :key="service.id"
                  class="flex items-center w-full h-[22px] mb-2 last:!mb-0"
                >
                  <img
                    :class="[$style['ops-aml-turnaround__content__delete-icon']]"
                    :src="getImageUrl(`assets/icons/close-circle-outline.svg`)"
                    alt="disapprove"
                    @click="onRemoveService(index)"
                  />

                  <ULabel
                    text-class="mb-0"
                    :required="false"
                    :label-text="findServiceNameById(service.service).name"
                  />
                </div>
              </div>
              <div class="mt-2">
                <div
                  v-for="service in missionFormModel.legs[legIndex].servicing.services"
                  :key="service.id"
                >
                  <div class="flex justify-between gap-[0.75rem] items-center pr-1 mb-2">
                    <UCheckboxWrapper
                      v-model="service.on_arrival"
                      :disabled="isDisabledField || !findServiceNameById(service.service).arrival"
                      class="gap-0 mr-2 !mb-0 d-flex"
                      size="24px"
                    />
                    <UCheckboxWrapper
                      v-model="service.on_departure"
                      :disabled="isDisabledField || !findServiceNameById(service.service).departure"
                      class="gap-0 !mb-0"
                      size="24px"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="h-[360px]">
        <div :class="[$style['ops-aml-turnaround__error']]">Servicing is disabled</div>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed, onMounted, PropType, ref, watch } from 'vue'
import { getImageUrl } from '@/helpers'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import USelectWrapper from '@/components/ui/wrappers/USelectWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { storeToRefs } from 'pinia'
import {
  FuelRequiredTypes,
  missionDefaultFormModel,
  missionLegServicingDefaults
} from '@/constants/mission.constants'
import { useFetch } from '@/composables/useFetch'
import ULabel from '@/components/ui/form/ULabel.vue'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import MissionReferences from '@/services/mission/mission-references'
import { ErrorObject } from '@vuelidate/core'
import type { IService } from '@/types/mission/mission-reference.types'
import { IAirport } from '@/types/mission/airport.types'
import type { ILegService, ServiceFuelingType } from '@/types/mission/mission.types'
import { getMissionId } from '@/helpers'
const props = defineProps({
  legSequenceId: {
    type: Number,
    default: 0
  },
  legIndex: {
    type: Number,
    default: 0
  },
  leg: {
    type: Object,
    default: () => ({})
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => {}
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  }
})

const missionFormStore = useMissionFormStore()
const missionReferenceStore = useMissionReferenceStore()
const { isLoadingQuantityUnits, quantityUnits } = storeToRefs(missionReferenceStore)
const { formModel: missionFormModel } = storeToRefs(missionFormStore)
const missionsReferenceStore = useMissionReferenceStore()
const { airportLocations } = storeToRefs(missionsReferenceStore)
const searchPristQuery = ref('')
const {
  loading: isLoadingServices,
  data: serviceOptions,
  callFetch: fetchServices
} = useFetch<IService[], (locationId: number, organisationId?: number) => void>(
  async (locationId: number, organisationId?: number) => {
    const { data } = await MissionReferences.fetchServices(locationId, organisationId)
    return data
  }
)

const computedFilteredServiceOptions = computed(() =>
  serviceOptions.value?.filter((option: IService) => {
    return !(computedLegInfo.value?.servicing?.services as ILegService[])?.some(
      (service) => service?.service === option.id
    )
  })
)

const computedLegInfo = computed(() => missionFormModel.value?.legs?.[props.legIndex])

const isAmlServicingEnabled = computed<boolean>(
  () => computedLegInfo.value.arrival_location && computedLegInfo.value.arrival_aml_service
)

const onHandleAmlServicing = () => {
  if (getMissionId() && props.leg?.sequence_id !== undefined) {
    isAmlServicingEnabled.value ? onCancelServicing() : onToggleAmlServicing(true)
    return
  }
  return onToggleAmlServicing(!isAmlServicingEnabled.value)
}
const arrivalAirportShortName = computed(() => {
  return (
    (airportLocations.value &&
      airportLocations.value?.find((airport: IAirport) => {
        return airport.id === computedLegInfo.value?.arrival_location?.id ? airport : ''
      })?.tiny_repr) ||
    ''
  )
})

const isDisabledField = computed(() => {
  return !isAmlServicingEnabled.value || !computedLegInfo.value?.arrival_location
})

const isFuelingDisabled = computed(() => computedLegInfo.value?.servicing.fuel_required === null)

const onToggleAmlServicing = (flag: boolean) => {
  missionFormModel.value.legs[props.legIndex].arrival_aml_service = flag
  if (flag)
    return (missionFormModel.value.legs[props.legIndex].servicing = missionLegServicingDefaults())
  delete missionFormModel.value.legs[props.legIndex].servicing

  // if (!flag) {
  //   missionFormModel.value.legs[props.legIndex].servicing = missionLegServicingDefaults()
  // }
}

const onChangeFuellingType = (type: ServiceFuelingType) => {
  if (type === null) {
    missionFormModel.value.legs[props.legIndex].servicing.fuel_quantity = 0
    missionFormModel.value.legs[props.legIndex].servicing.fuel_unit = null
  }
}
const onCancelServicing = async () => {
  const { isConfirmed } = await window.Swal({
    title: 'Confirmation',
    text: `Please confirm that you wish cancel the servicing & fueling arrangements at ${
      arrivalAirportShortName.value
    } for legs ${props.legIndex + 1} & ${props.legIndex + 2}`,
    icon: 'info',
    showCancelButton: true
  })
  if (isConfirmed) {
    onToggleAmlServicing(false)
  }
}

const onRemoveService = (serviceIndex: number) => {
  missionFormModel.value.legs[props.legIndex].servicing?.services.splice(serviceIndex, 1)
}

const findServiceNameById = (
  id: string
): { name: string; arrival: boolean; departure: boolean } => {
  const res = (serviceOptions.value as IService[])?.find((option: IService) => option.id === id)
  const availability = res?.attributes?.availability_bool?.find(
    (item) => item.airport === computedLegInfo.value.arrival_location
  )
  return {
    arrival: true,
    departure: true,
    name: res?.attributes?.name || 'Unknown',
    ...(availability ? { arrival: availability.arrival, departure: availability.departure } : {})
  }
}

const onSearchPrist = (event: string) => {
  searchPristQuery.value = event
}
watch(
  () => [computedLegInfo.value?.arrival_location, missionFormModel.value?.organisation],
  async ([locationId, organisationId], [oldLocation]) => {
    if (!!oldLocation && locationId !== oldLocation) {
      missionFormModel.value.legs[props.legIndex].servicing.services = []
    }
    if (!locationId && props.legIndex + 1 !== missionFormModel.value?.legs?.length) {
      return (missionFormModel.value.legs[props.legIndex].servicing = missionLegServicingDefaults())
    }
    await fetchServices(locationId, organisationId)
  }
)

onMounted(() => {
  if (!computedLegInfo.value?.arrival_location && !missionFormModel.value?.organisation) return
  fetchServices(
    computedLegInfo.value?.arrival_location,
    missionFormModel.value?.organisation as any
  )
})
</script>
<style lang="scss" module>
.ops-aml-turnaround {
  &-wrapper {
    @apply flex rounded-[0.5rem] flex-col bg-white min-w-0;
  }

  &__content {
    @apply font-medium text-[1.25rem] h-auto  py-[1.25rem] pb-[1.375rem] text-grey-1000;
    &__delete-icon {
      @apply w-[18px] mr-2 cursor-pointer aspect-square;
      filter: invert(23%) sepia(85%) saturate(2552%) hue-rotate(330deg) brightness(87%)
        contrast(103%);
    }
  }
  &__error {
    @apply absolute z-50 opacity-100 text-[14px] text-[#97650e] w-[95%] text-center p-4 rounded-[0.5rem] top-[48%] left-1/2 -translate-y-[50%] -translate-x-[50%] border-[#fee5ba] bg-[#feeed1];
  }
}
</style>
