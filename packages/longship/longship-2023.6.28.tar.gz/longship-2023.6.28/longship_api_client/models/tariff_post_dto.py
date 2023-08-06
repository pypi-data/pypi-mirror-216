from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.tariff_post_dto_usage_type import TariffPostDtoUsageType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.private_emp_tariff_dto import PrivateEmpTariffDto


T = TypeVar("T", bound="TariffPostDto")


@attr.s(auto_attribs=True)
class TariffPostDto:
    """
    Attributes:
        name (Union[Unset, str]):
        currency (Union[Unset, str]):
        usage_type (Union[Unset, TariffPostDtoUsageType]):  Default: TariffPostDtoUsageType.SELL.
        private_emp_tariff (Union[Unset, PrivateEmpTariffDto]):
        start_tariff (Union[Unset, float]):
        price (Union[Unset, float]):
        parking_tariff (Union[Unset, float]):
        parking_step_size_in_minutes (Union[Unset, int]):
        parking_grace_period_in_minutes (Union[Unset, int]):
        time_tariff (Union[Unset, float]):
        time_step_size_in_minutes (Union[Unset, int]):
        time_grace_period_in_minutes (Union[Unset, int]):
        external_reference (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    currency: Union[Unset, str] = UNSET
    usage_type: Union[Unset, TariffPostDtoUsageType] = TariffPostDtoUsageType.SELL
    private_emp_tariff: Union[Unset, "PrivateEmpTariffDto"] = UNSET
    start_tariff: Union[Unset, float] = UNSET
    price: Union[Unset, float] = UNSET
    parking_tariff: Union[Unset, float] = UNSET
    parking_step_size_in_minutes: Union[Unset, int] = UNSET
    parking_grace_period_in_minutes: Union[Unset, int] = UNSET
    time_tariff: Union[Unset, float] = UNSET
    time_step_size_in_minutes: Union[Unset, int] = UNSET
    time_grace_period_in_minutes: Union[Unset, int] = UNSET
    external_reference: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        currency = self.currency
        usage_type: Union[Unset, str] = UNSET
        if not isinstance(self.usage_type, Unset):
            usage_type = self.usage_type.value

        private_emp_tariff: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.private_emp_tariff, Unset):
            private_emp_tariff = self.private_emp_tariff.to_dict()

        start_tariff = self.start_tariff
        price = self.price
        parking_tariff = self.parking_tariff
        parking_step_size_in_minutes = self.parking_step_size_in_minutes
        parking_grace_period_in_minutes = self.parking_grace_period_in_minutes
        time_tariff = self.time_tariff
        time_step_size_in_minutes = self.time_step_size_in_minutes
        time_grace_period_in_minutes = self.time_grace_period_in_minutes
        external_reference = self.external_reference

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if currency is not UNSET:
            field_dict["currency"] = currency
        if usage_type is not UNSET:
            field_dict["usageType"] = usage_type
        if private_emp_tariff is not UNSET:
            field_dict["privateEmpTariff"] = private_emp_tariff
        if start_tariff is not UNSET:
            field_dict["startTariff"] = start_tariff
        if price is not UNSET:
            field_dict["price"] = price
        if parking_tariff is not UNSET:
            field_dict["parkingTariff"] = parking_tariff
        if parking_step_size_in_minutes is not UNSET:
            field_dict["parkingStepSizeInMinutes"] = parking_step_size_in_minutes
        if parking_grace_period_in_minutes is not UNSET:
            field_dict["parkingGracePeriodInMinutes"] = parking_grace_period_in_minutes
        if time_tariff is not UNSET:
            field_dict["timeTariff"] = time_tariff
        if time_step_size_in_minutes is not UNSET:
            field_dict["timeStepSizeInMinutes"] = time_step_size_in_minutes
        if time_grace_period_in_minutes is not UNSET:
            field_dict["timeGracePeriodInMinutes"] = time_grace_period_in_minutes
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.private_emp_tariff_dto import PrivateEmpTariffDto

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        currency = d.pop("currency", UNSET)

        _usage_type = d.pop("usageType", UNSET)
        usage_type: Union[Unset, TariffPostDtoUsageType]
        if isinstance(_usage_type, Unset):
            usage_type = UNSET
        else:
            usage_type = TariffPostDtoUsageType(_usage_type)

        _private_emp_tariff = d.pop("privateEmpTariff", UNSET)
        private_emp_tariff: Union[Unset, PrivateEmpTariffDto]
        if isinstance(_private_emp_tariff, Unset):
            private_emp_tariff = UNSET
        else:
            private_emp_tariff = PrivateEmpTariffDto.from_dict(_private_emp_tariff)

        start_tariff = d.pop("startTariff", UNSET)

        price = d.pop("price", UNSET)

        parking_tariff = d.pop("parkingTariff", UNSET)

        parking_step_size_in_minutes = d.pop("parkingStepSizeInMinutes", UNSET)

        parking_grace_period_in_minutes = d.pop("parkingGracePeriodInMinutes", UNSET)

        time_tariff = d.pop("timeTariff", UNSET)

        time_step_size_in_minutes = d.pop("timeStepSizeInMinutes", UNSET)

        time_grace_period_in_minutes = d.pop("timeGracePeriodInMinutes", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        tariff_post_dto = cls(
            name=name,
            currency=currency,
            usage_type=usage_type,
            private_emp_tariff=private_emp_tariff,
            start_tariff=start_tariff,
            price=price,
            parking_tariff=parking_tariff,
            parking_step_size_in_minutes=parking_step_size_in_minutes,
            parking_grace_period_in_minutes=parking_grace_period_in_minutes,
            time_tariff=time_tariff,
            time_step_size_in_minutes=time_step_size_in_minutes,
            time_grace_period_in_minutes=time_grace_period_in_minutes,
            external_reference=external_reference,
        )

        tariff_post_dto.additional_properties = d
        return tariff_post_dto

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
