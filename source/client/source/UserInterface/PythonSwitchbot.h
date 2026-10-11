#pragma once

#ifdef ENABLE_SWITCHBOT

class CPythonSwitchbot : public CSingleton <CPythonSwitchbot>
{
public:
#pragma pack(1)
	struct TSwitchbotAttributeAlternativeTable
	{
		TPlayerItemAttribute attributes[MAX_NORM_ATTR_NUM];

		bool IsConfigured() const
		{
			for (const auto& it : attributes)
			{
				if (it.bType && it.sValue)
				{
					return true;
				}
			}

			return false;
		}
	};

	struct TSwitchbotTable
	{
		uint32_t player_id;
		bool active[SWITCHBOT_SLOT_COUNT];
		bool finished[SWITCHBOT_SLOT_COUNT];
		uint32_t items[SWITCHBOT_SLOT_COUNT];
		TSwitchbotAttributeAlternativeTable alternatives[SWITCHBOT_SLOT_COUNT][SWITCHBOT_ALTERNATIVE_COUNT];

		TSwitchbotTable() : player_id(0)
		{
			memset(&items, 0, sizeof(items));
			memset(&alternatives, 0, sizeof(alternatives));
			memset(&active, false, sizeof(active));
			memset(&finished, false, sizeof(finished));
		}
	};

	struct TSwitchbottAttributeTable
	{
		uint8_t attribute_set;
		int32_t apply_num;
		uint32_t max_value;
	};

#pragma pack()

	CPythonSwitchbot();
	virtual ~CPythonSwitchbot();

	void Initialize();
	void Update(const TSwitchbotTable& table);

	void SetAttribute(uint8_t slot, uint8_t alternative, uint8_t attrIdx, uint8_t attrType, int32_t attrValue);
	TPlayerItemAttribute GetAttribute(uint8_t slot, uint8_t alternative, uint8_t attrIdx);
	void GetAlternatives(uint8_t slot, std::vector<TSwitchbotAttributeAlternativeTable>& attributes);
	int32_t GetAttibuteSet(uint8_t slot);
	bool IsActive(uint8_t slot);
	bool IsFinished(uint8_t slot);

	void ClearSlot(uint8_t slot);
	void ClearAttributeMap();

	void AddAttributeToMap(const TSwitchbottAttributeTable& table);
	void GetAttributesBySet(int32_t iAttributeSet, std::vector<TPlayerItemAttribute>& vec_attributes);
	uint32_t GetAttributeMaxValue(int32_t iAttributeSet, uint8_t attrType);

protected:
	TSwitchbotTable m_SwitchbotTable;
	std::map<uint8_t, std::map<uint8_t, uint32_t>> m_map_AttributesBySet;
};
#endif