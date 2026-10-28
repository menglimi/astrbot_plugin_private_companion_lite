# Lite 核心配置指南

在 AstrBot 插件配置中展开“核心偏好”，添加条目，填写配置组、生效范围与设置值。保存后重载插件。

## 使用规则

- `installation`：整个安装的默认值，不需要目标和角色 ID。
- `role`：角色的偏好，需要账号与会话中已有的 `target_id` 和人格映射的 `role_id`。
- `relationship`：角色与一个私聊对象的关系偏好，需要目标与角色。
- `window` / `scope`：指定私聊会话的偏好，需要目标与角色。群聊设置使用 `role` 范围，填写群目标 ID 和其人格对应角色；无需等待群友先发言。
- 每个配置组只接受下表列出的范围；设置值是 JSON 对象，使用完整字段 ID。
- 只填写需要更改的字段。删除条目或留空列表会保留已保存的值；清空某个覆盖值请把字段 ID 填入“恢复继承的字段 ID”。
- 同一范围内同一组只添加一项；不合法配置整体回滚，并在日志报告错误。
- 同一配置再次加载不会重复写入已经生效的普通值。设置值的优先级由现有核心配置合同决定，已保存的角色或会话值可覆盖安装默认值。
- 这些条目由管理员配置文件加载，不授予聊天用户配置管理员权限。

## 常用示例

主动联系：配置组 `proactive.contact`、范围 `installation`，设置值可填写：

```json
{"proactive.contact.enabled": true}
```

主动联系还需要用户授权。新安装默认不主动联系：添加另一条配置，组为 `private_access`、范围 `installation`，值为 `{"private_access.proactive_default": true}`，随后保存重载并在对应私聊发送一条消息。这个默认值仅对尚未做过单独权限决定的用户生效，已明确撤销的权限保持撤销。需要恢复旧版逐人撤销的权限时，请通过完整版管理。

主动联系仍需已有的私聊目标、人格与发送权限，并遵循安静时段、额度和语境判断。将第一条例子的 `proactive.contact.enabled` 改为 `false` 可关闭主动生成。

其他分段与语音基本设置优先使用官方配置页的“分段”和“语音回复”分组；高级覆盖值可用下方 `conversation.reply` 组。人格正文继续在 AstrBot 人格管理中维护。

## 字段参考

下表从本版实际运行时注册的字段生成。默认值不代表现有资料当前的值。`text` 中保存 JSON 的字段，值本身仍需是 JSON 字符串。概率范围是 0～1。

### conversation.busy_gate

生效范围：role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.busy_gate.busy_reply_gate_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.busy_gate.busy_reply_min_delay_seconds` | integer | `60` | ≥ 0；≤ 900 |
| `conversation.busy_gate.busy_reply_max_delay_seconds` | integer | `300` | ≥ 0；≤ 900 |
| `conversation.busy_gate.busy_reply_proactive_resume_buffer_minutes` | integer | `10` | ≥ 0；≤ 120 |
| `conversation.busy_gate.busy_activity_keywords` | text | `"[\"上课\", \"课堂\", \"听课\", \"自习\", \"学习\", \"复习\", \"预习\", \"写作业\", \"做作业\", \"赶作业\", \"做题\", \"考试\", \"测验\", \"开会\", \"会议\", \"工作\", \"办公\", \"值班\", \"实习\", …` | 按领域规则校验 |
| `conversation.busy_gate.busy_exclude_keywords` | text | `"[\"睡觉\", \"睡眠\", \"午睡\", \"午休\", \"补觉\", \"休息\", \"发呆\", \"摸鱼\", \"放松\", \"吃饭\", \"用餐\", \"散步\", \"刷视频\", \"看番\", \"打游戏\", \"玩游戏\", \"聊天\", \"自由时间\", \"准备睡\…` | 按领域规则校验 |
| `conversation.busy_gate.busy_urgent_keywords` | text | `"[\"救命\", \"出事\", \"紧急\", \"急事\", \"报警\", \"医院\", \"受伤\", \"流血\", \"疼得\", \"不舒服\", \"呼吸困难\", \"害怕\", \"崩溃\", \"自杀\", \"不想活\", \"马上回\", \"立刻回\", \"快回\", \"现在就…` | 按领域规则校验 |

### conversation.group_participation

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.group_participation.enable_group_social_context` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.enable_group_topic_threads` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.group_topic_thread_max` | integer | `12` | ≥ 3；≤ 40 |
| `conversation.group_participation.enable_group_mood_detection` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.enable_group_roleplay_strength` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.enable_group_moments` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.enable_group_moment_portrait` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.enable_group_joke_guard` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.enable_group_persona_denoise` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.enable_group_interjection` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.group_interject_min_interval_minutes` | integer | `180` | ≥ 0；≤ 1440 |
| `conversation.group_participation.group_interject_max_daily` | integer | `2` | ≥ 0；≤ 20 |
| `conversation.group_participation.enable_group_interjection_feedback` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.group_interject_feedback_window_seconds` | integer | `600` | ≥ 60；≤ 86400 |
| `conversation.group_participation.enable_group_repeat_follow` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_count_distinct_users_only` | boolean | `false` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_trigger_threshold` | integer | `4` | ≥ 3；≤ 20 |
| `conversation.group_participation.group_repeat_follow_probability` | probability | `0.18` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_interrupt_probability` | probability | `0.1` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_interrupt_probability_step` | probability | `0.12` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_interrupt_text` | text | `"禁止复读"` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_interrupt_image_path` | text | `""` | 按领域规则校验 |
| `conversation.group_participation.group_repeat_window_seconds` | integer | `120` | ≥ 10；≤ 600 |
| `conversation.group_participation.group_context_max_age_hours` | integer | `12` | ≥ 1；≤ 168 |
| `conversation.group_participation.enable_group_behavior_learning` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.enable_group_behavior_imitation` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.enable_group_behavior_feedback` | boolean | `true` | 按领域规则校验 |
| `conversation.group_participation.group_behavior_guidance` | text | `""` | 文本上限 1200 |

### conversation.image_review

生效范围：role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.image_review.enable_group_nsfw_private_fallback` | boolean | `false` | 按领域规则校验 |
| `conversation.image_review.group_nsfw_image_review_mode` | text | `"single"` | 按领域规则校验 |
| `conversation.image_review.group_nsfw_image_review_sensitivity` | text | `"balanced"` | 按领域规则校验 |
| `conversation.image_review.group_nsfw_image_review_min_confidence` | probability | `0.7` | ≥ 0.0；≤ 1.0 |
| `conversation.image_review.group_nsfw_image_review_timeout_seconds` | weight | `8.0` | ≥ 3.0；≤ 30.0 |
| `conversation.image_review.group_nsfw_image_review_max_dimension` | integer | `1280` | ≥ 0；≤ 4096 |
| `conversation.image_review.group_nsfw_image_review_max_images` | integer | `1` | ≥ 1；≤ 8 |
| `conversation.image_review.group_nsfw_image_review_failure_action` | text | `"private"` | 按领域规则校验 |
| `conversation.image_review.group_nsfw_image_review_custom_prompt` | text | `""` | 按领域规则校验 |
| `conversation.image_review.review_provider` | text | `""` | 按领域规则校验 |
| `conversation.image_review.review_dual_provider` | text | `""` | 按领域规则校验 |

### conversation.media_quota

生效范围：installation, role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.media_quota.private_owner_max_daily` | integer | `-1` | ≥ -1；≤ 100 |
| `conversation.media_quota.private_friend_max_daily` | integer | `-1` | ≥ -1；≤ 100 |
| `conversation.media_quota.group_max_daily` | integer | `-1` | ≥ -1；≤ 100 |
| `conversation.media_quota.proactive_max_daily` | integer | `-1` | ≥ -1；≤ 100 |

### conversation.perception

生效范围：role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.perception.calendar_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.calendar_timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `conversation.perception.holiday_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.holiday_country` | text | `"CN"` | 按领域规则校验 |
| `conversation.perception.lunar_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.automatic_solar_terms_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.almanac_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.perception.platform_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.model_route_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.configured_modalities_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.perception.guidance` | text | `""` | 按领域规则校验 |

### conversation.presentation

生效范围：role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.presentation.enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.llm_controlled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.rules_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.rule_mode` | text | `"words"` | 按领域规则校验 |
| `conversation.presentation.split_words` | text | `"[\"。\", \"？\", \"！\", \"~\", \"～\", \"?\", \".\", \"!\", \";\", \"；\", \"……\", \"）\", \"…\"]"` | 按领域规则校验 |
| `conversation.presentation.match_width_variants` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.rule_regex` | text | `"(?<=[。！？!?…~～])\\s*\|\\n+"` | 按领域规则校验 |
| `conversation.presentation.threshold` | integer | `500` | ≥ 1；≤ 65536 |
| `conversation.presentation.min_segment_chars` | integer | `5` | ≥ 1；≤ 65536 |
| `conversation.presentation.max_segments` | integer | `5` | ≥ 1；≤ 64 |
| `conversation.presentation.prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.streaming_mode` | text | `"buffered"` | 按领域规则校验 |
| `conversation.presentation.streaming` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.part_gap_ms` | integer | `0` | ≥ 0；≤ 60000 |
| `conversation.presentation.part_gap_mode` | text | `"log"` | 按领域规则校验 |
| `conversation.presentation.part_gap_min_ms` | integer | `1500` | ≥ 100；≤ 60000 |
| `conversation.presentation.part_gap_max_ms` | integer | `3500` | ≥ 100；≤ 60000 |
| `conversation.presentation.part_gap_log_base` | weight | `2.1` | ≥ 1.1；≤ 5.0 |
| `conversation.presentation.image_position` | text | `"after_text"` | 按领域规则校验 |
| `conversation.presentation.voice_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.voice_trigger_mode` | text | `"always"` | 按领域规则校验 |
| `conversation.presentation.voice_generation_mode` | text | `"plain"` | 按领域规则校验 |
| `conversation.presentation.voice_conversion_scope` | text | `"full"` | 按领域规则校验 |
| `conversation.presentation.voice_segment_mode` | text | `"whole"` | 按领域规则校验 |
| `conversation.presentation.voice_delivery_mode` | text | `"voice_and_text"` | 按领域规则校验 |
| `conversation.presentation.voice_position` | text | `"after_media"` | 按领域规则校验 |
| `conversation.presentation.voice_language` | text | `"zh"` | 按领域规则校验 |
| `conversation.presentation.voice_foreign_text_mode` | text | `"original"` | 按领域规则校验 |
| `conversation.presentation.voice_probability` | probability | `1.0` | 按领域规则校验 |
| `conversation.presentation.voice_cooldown_seconds` | integer | `0` | ≥ 0；≤ 86400 |
| `conversation.presentation.voice_max_speech_chars` | integer | `1800` | ≥ 1；≤ 10000 |
| `conversation.presentation.voice_timeout_seconds` | integer | `30` | ≥ 1；≤ 120 |
| `conversation.presentation.voice_trigger_keywords` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_primary_mention_keywords` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_primary_mention_probability` | probability | `0.8` | 按领域规则校验 |
| `conversation.presentation.voice_primary_mention_prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_zh_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_ja_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_en_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_private_zh_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_private_ja_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_private_en_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_group_zh_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_group_ja_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_group_en_provider_id` | text | `""` | 按领域规则校验 |
| `conversation.presentation.voice_extra_prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.group_air_guard_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.group_air_guard_window_seconds` | integer | `60` | ≥ 30；≤ 1800 |
| `conversation.presentation.group_air_guard_max_bot_replies` | integer | `3` | ≥ 1；≤ 20 |
| `conversation.presentation.group_air_guard_cooldown_seconds` | integer | `150` | ≥ 0；≤ 1800 |
| `conversation.presentation.group_air_guard_polite_loop_limit` | integer | `2` | ≥ 1；≤ 10 |
| `conversation.presentation.group_high_intensity_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.group_conversation_followup_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.group_conversation_followup_seconds` | integer | `120` | ≥ 15；≤ 1800 |
| `conversation.presentation.group_conversation_followup_max_turns` | integer | `3` | ≥ 1；≤ 12 |
| `conversation.presentation.private_closing_guard_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.private_closing_guard_window_seconds` | integer | `1800` | ≥ 60；≤ 7200 |
| `conversation.presentation.private_closing_guard_prompt_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.private_debounce_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.private_debounce_min_ms` | integer | `1500` | ≥ 10；≤ 120000 |
| `conversation.presentation.private_debounce_max_ms` | integer | `4000` | ≥ 10；≤ 120000 |
| `conversation.presentation.private_debounce_total_ms` | integer | `8000` | ≥ 10；≤ 120000 |
| `conversation.presentation.group_wakeup_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_direct_words` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_context_words` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_interest_keywords` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_question_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_bot_name` | text | `""` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_primary_member_ids` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_owner_direct_words` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_interest_probability` | probability | `0.18` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_question_threshold` | integer | `65` | ≥ 0；≤ 100 |
| `conversation.presentation.group_wakeup_cold_group_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_cold_group_threshold` | integer | `65` | ≥ 0；≤ 100 |
| `conversation.presentation.group_wakeup_cold_group_idle_minutes` | integer | `25` | ≥ 3；≤ 720 |
| `conversation.presentation.group_wakeup_cooldown_seconds` | integer | `90` | ≥ 0；≤ 3600 |
| `conversation.presentation.group_wakeup_fatigue_limit` | integer | `5` | ≥ 1；≤ 20 |
| `conversation.presentation.group_wakeup_fatigue_decay_minutes` | integer | `90` | ≥ 5；≤ 720 |
| `conversation.presentation.group_wakeup_bot_name_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_generated_keyword_limit` | integer | `24` | ≥ 4；≤ 80 |
| `conversation.presentation.group_wakeup_topic_interest_max_boost` | integer | `45` | ≥ 0；≤ 150 |
| `conversation.presentation.group_wakeup_debounce_pending_penalty` | integer | `65` | ≥ 0；≤ 100 |
| `conversation.presentation.group_wakeup_image_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_image_weight` | probability | `0.2` | 按领域规则校验 |
| `conversation.presentation.group_wakeup_short_text_wait_ms` | integer | `15000` | ≥ 0；≤ 30000 |
| `conversation.presentation.group_wakeup_log_limit` | integer | `80` | ≥ 10；≤ 300 |
| `conversation.presentation.enable_group_injection_guard` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.enable_group_privacy_guard` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.enable_group_reality_promise_guard` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.recall_silence_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.component_order` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.reply_quote_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.reply_quote_group_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.reply_quote_first_part_only` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.reply_quote_skip_chars` | integer | `0` | ≥ 0；≤ 120 |
| `conversation.presentation.reply_mention_speaker_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.content_cleanup_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.content_cleanup_mode` | text | `"words"` | 按领域规则校验 |
| `conversation.presentation.content_cleanup_scope` | text | `"trailing"` | 按领域规则校验 |
| `conversation.presentation.content_cleanup_rule` | text | `"[\\n]"` | 按领域规则校验 |
| `conversation.presentation.content_cleanup_words` | text | `"[\"\\n\"]"` | 按领域规则校验 |
| `conversation.presentation.content_replacement_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.content_replacements` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.framework_error_guard_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.enable_forbidden_word_recall` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.recall_forbidden_words` | text | `"[]"` | 按领域规则校验 |
| `conversation.presentation.recall_forbidden_scope` | text | `"bot_and_group"` | 按领域规则校验 |
| `conversation.presentation.recall_forbidden_word_case_sensitive` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.style_prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.prompt_style_mode` | text | `"free"` | 按领域规则校验 |
| `conversation.presentation.enable_humanized_expression` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.humanized_expression_prompt` | text | `"沿用当前人格的用词、性格和关系距离；这些要求只影响表达，不改变事实、来源、权限或本轮任务。\n日常聊天先回应对方此刻最想说的一点，再给出自己的具体反应；需要确认理解时简短核对，平常不要先复述或总结对方的话。可以好奇、打趣、护短、偏心、认真或安静，情绪有来由，也可顺手带出自己刚经历的小事或想法，不把每句话改写成摘…` | 按领域规则校验 |
| `conversation.presentation.forward_message_adaptation_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.enable_context_image_captioning` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.context_image_caption_max_items` | integer | `2` | ≥ 0；≤ 8 |
| `conversation.presentation.enable_private_image_self_recognition` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.enable_private_image_vision_cache` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.private_image_vision_cache_max_items` | integer | `300` | ≥ 0；≤ 2000 |
| `conversation.presentation.private_image_vision_custom_prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.private_image_vision_max_chars` | integer | `1200` | ≥ 120；≤ 4000 |
| `conversation.presentation.private_image_vision_wait_seconds` | integer | `8` | ≥ 1；≤ 30 |
| `conversation.presentation.private_image_provider_failure_cooldown_seconds` | integer | `60` | ≥ 0；≤ 3600 |
| `conversation.presentation.private_image_self_recognition_hint` | text | `""` | 按领域规则校验 |
| `conversation.presentation.video_understanding_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.video_understanding_max_chars` | integer | `2400` | ≥ 200；≤ 6000 |
| `conversation.presentation.video_understanding_wait_seconds` | integer | `20` | ≥ 1；≤ 60 |
| `conversation.presentation.video_understanding_prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.video_self_recognition_hint` | text | `""` | 按领域规则校验 |
| `conversation.presentation.image_understanding_private_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.image_understanding_group_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.astrbot_animated_image_understanding_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.video_understanding_private_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.video_understanding_group_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.file_understanding_private_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.file_understanding_group_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.presentation.file_understanding_enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.presentation.file_understanding_formats` | text | `"text_and_documents"` | 按领域规则校验 |
| `conversation.presentation.file_understanding_format_groups` | text | `"文本\nPDF\nWord（DOCX）\nExcel（XLSX）\nPowerPoint（PPTX）"` | 按领域规则校验 |
| `conversation.presentation.file_understanding_max_size_mb` | integer | `8` | ≥ 1；≤ 16 |
| `conversation.presentation.file_understanding_max_chars` | integer | `24000` | ≥ 1000；≤ 48000 |
| `conversation.presentation.file_understanding_timeout_seconds` | integer | `15` | ≥ 1；≤ 30 |
| `conversation.presentation.file_understanding_prompt` | text | `""` | 按领域规则校验 |
| `conversation.presentation.reply_diagnostic_limit` | integer | `80` | ≥ 10；≤ 300 |

### conversation.recall

生效范围：window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.recall.transcribe_enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.recall.transcribe_max_items` | integer | `5` | ≥ 1；≤ 20 |
| `conversation.recall.transcribe_text_chars` | integer | `500` | ≥ 80；≤ 2000 |
| `conversation.recall.transcribe_window_minutes` | integer | `10` | ≥ 1；≤ 1440 |

### conversation.relay

生效范围：window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.relay.enabled` | boolean | `false` | 按领域规则校验 |
| `conversation.relay.require_confirm` | boolean | `true` | 按领域规则校验 |
| `conversation.relay.max_text_chars` | integer | `500` | ≥ 20；≤ 2000 |
| `conversation.relay.allowed_targets` | text | `""` | 按领域规则校验 |
| `conversation.relay.allowed_groups` | text | `""` | 按领域规则校验 |
| `conversation.relay.member_cache_minutes` | integer | `60` | ≥ 1；≤ 1440 |
| `conversation.relay.prefer_relationship_names` | boolean | `true` | 按领域规则校验 |
| `conversation.relay.multi_target_limit` | integer | `5` | ≥ 1；≤ 20 |
| `conversation.relay.default_style` | text | `"persona"` | 按领域规则校验 |
| `conversation.relay.core_target_id` | text | `""` | 按领域规则校验 |

### conversation.web

生效范围：window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `conversation.web.enabled` | boolean | `true` | 按领域规则校验 |
| `conversation.web.max_links` | integer | `2` | ≥ 1；≤ 5 |
| `conversation.web.max_chars` | integer | `4000` | ≥ 200；≤ 8000 |
| `conversation.web.timeout_seconds` | integer | `8` | ≥ 3；≤ 30 |

### expression.learning

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `expression.learning.private_learning_enabled` | boolean | `true` | 按领域规则校验 |
| `expression.learning.group_learning_enabled` | boolean | `false` | 按领域规则校验 |
| `expression.learning.private_application_enabled` | boolean | `true` | 按领域规则校验 |
| `expression.learning.group_application_enabled` | boolean | `true` | 按领域规则校验 |
| `expression.learning.sample_review_enabled` | boolean | `false` | 按领域规则校验 |
| `expression.learning.style_review_enabled` | boolean | `true` | 按领域规则校验 |
| `expression.learning.window_hours` | integer | `720` | ≥ 1；≤ 720 |
| `expression.learning.sample_limit` | integer | `60` | ≥ 4；≤ 64 |
| `expression.learning.min_samples` | integer | `2` | ≥ 1；≤ 16 |
| `expression.learning.group_min_samples` | integer | `20` | ≥ 5；≤ 64 |
| `expression.learning.sample_chars` | integer | `800` | ≥ 40；≤ 4000 |
| `expression.learning.active_signal_limit` | integer | `60` | ≥ 12；≤ 480 |
| `expression.learning.rules_per_turn` | integer | `2` | ≥ 1；≤ 16 |
| `expression.learning.payload_chars` | integer | `4000` | ≥ 500；≤ 16000 |
| `expression.learning.rotation_candidate_limit` | integer | `24` | ≥ 1；≤ 64 |
| `expression.learning.rotation_decay_hours` | integer | `336` | ≥ 1；≤ 8760 |
| `expression.learning.scan_interval_minutes` | integer | `90` | ≥ 5；≤ 10080 |
| `expression.learning.group_scan_interval_minutes` | integer | `180` | ≥ 5；≤ 10080 |
| `expression.learning.group_daily_batch_limit` | integer | `6` | ≥ 1；≤ 50 |
| `expression.learning.group_new_messages` | integer | `20` | ≥ 5；≤ 80 |
| `expression.learning.learning_mode` | text | `"balanced"` | 文本上限 16 |

### expression.learning.group

生效范围：window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `expression.learning.group.group_learning_enabled` | boolean | `false` | 按领域规则校验 |
| `expression.learning.group.group_member_mode` | text | `"all"` | 文本上限 16 |
| `expression.learning.group.group_member_ids` | text | `""` | 文本上限 4000 |

### expression.learning.private

生效范围：relationship。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `expression.learning.private.private_learning_enabled` | boolean | `true` | 按领域规则校验 |

### expression.reaction

生效范围：installation。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `expression.reaction.low_latency_enabled` | boolean | `true` | 按领域规则校验 |
| `expression.reaction.embedding_backfill_enabled` | boolean | `true` | 按领域规则校验 |
| `expression.reaction.candidate_limit` | integer | `6` | ≥ 1；≤ 24 |
| `expression.reaction.embedding_candidate_limit` | integer | `1200` | ≥ 20；≤ 5000 |
| `expression.reaction.embedding_backfill_batch_size` | integer | `24` | ≥ 1；≤ 100 |
| `expression.reaction.embedding_backfill_interval_seconds` | integer | `300` | ≥ 0；≤ 86400 |
| `expression.reaction.embedding_weight` | weight | `1.0` | ≥ 0.05；≤ 3.0 |
| `expression.reaction.embedding_score_threshold` | probability | `0.42` | ≥ 0.0；≤ 1.0 |
| `expression.reaction.vision_verify_mode` | text | `"embedding"` | 按领域规则校验 |

### knowledge

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `knowledge.import_enabled` | boolean | `false` | 按领域规则校验 |
| `knowledge.inject_enabled` | boolean | `true` | 按领域规则校验 |
| `knowledge.member_recognition_enabled` | boolean | `false` | 按领域规则校验 |
| `knowledge.member_match_aliases` | boolean | `true` | 按领域规则校验 |
| `knowledge.import_paths` | text | `""` | 按领域规则校验 |
| `knowledge.source_ids` | text | `""` | 按领域规则校验 |
| `knowledge.entry_limit` | integer | `500` | ≥ 1；≤ 5000 |
| `knowledge.entry_char_limit` | integer | `1200` | ≥ 64；≤ 4000 |
| `knowledge.source_limit` | integer | `16` | ≥ 1；≤ 64 |
| `knowledge.candidate_char_budget` | integer | `60000` | ≥ 2000；≤ 200000 |
| `knowledge.inject_max_entries` | integer | `8` | ≥ 1；≤ 24 |
| `knowledge.inject_max_chars` | integer | `6000` | ≥ 500；≤ 24000 |
| `knowledge.member_inject_limit` | integer | `6` | ≥ 1；≤ 12 |
| `knowledge.member_clue_chars` | integer | `1200` | ≥ 200；≤ 4000 |

### library

生效范围：role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `library.enabled` | boolean | `false` | 按领域规则校验 |
| `library.reviews_enabled` | boolean | `true` | 按领域规则校验 |
| `library.reading_excerpt_chars` | integer | `1200` | ≥ 200；≤ 8000 |
| `library.manual_entries_enabled` | boolean | `true` | 按领域规则校验 |
| `library.max_entries_per_page` | integer | `64` | ≥ 1；≤ 200 |
| `library.rating_enabled` | boolean | `false` | 按领域规则校验 |
| `library.preference_influence_enabled` | boolean | `false` | 按领域规则校验 |
| `library.preference_min_ratings` | integer | `5` | ≥ 1；≤ 64 |
| `library.preference_max_terms` | integer | `8` | ≥ 1；≤ 32 |
| `library.min_interval_hours` | integer | `18` | ≥ 1；≤ 720 |
| `library.share_probability` | probability | `0.18` | 按领域规则校验 |
| `library.ask_probability` | probability | `0.16` | 按领域规则校验 |

### memory

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `memory.enabled` | boolean | `true` | 按领域规则校验 |
| `memory.automatic_context` | boolean | `true` | 按领域规则校验 |
| `memory.context_items` | integer | `4` | ≥ 0；≤ 16 |
| `memory.context_chars` | integer | `6000` | ≥ 256；≤ 24000 |
| `memory.query_items` | integer | `20` | ≥ 1；≤ 50 |
| `memory.query_chars` | integer | `20000` | ≥ 256；≤ 48000 |
| `memory.source_chars` | integer | `8000` | ≥ 256；≤ 24000 |
| `memory.turn_chars` | integer | `64000` | ≥ 1024；≤ 200000 |
| `memory.turn_calls` | integer | `24` | ≥ 1；≤ 32 |
| `memory.core_items` | integer | `4` | ≥ 0；≤ 16 |
| `memory.core_chars` | integer | `6000` | ≥ 256；≤ 24000 |
| `memory.inclusion_chars` | integer | `24000` | ≥ 512；≤ 96000 |
| `memory.reflection_enabled` | boolean | `true` | 按领域规则校验 |
| `memory.reflection_timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `memory.reflection_time` | text | `"23:50"` | 按领域规则校验 |
| `memory.reflection_response_format` | text | `"text"` | 按领域规则校验 |
| `memory.reflection_auto_repair` | boolean | `true` | 按领域规则校验 |
| `memory.group_episode_memory_enabled` | boolean | `true` | 按领域规则校验 |
| `memory.group_episode_refresh_minutes` | integer | `180` | ≥ 30；≤ 1440 |
| `memory.group_episode_min_messages` | integer | `12` | ≥ 1；≤ 64 |
| `memory.max_group_episodes` | integer | `10` | ≥ 1；≤ 32 |
| `memory.dialogue_episode_memory_enabled` | boolean | `true` | 按领域规则校验 |
| `memory.dialogue_episode_refresh_messages` | integer | `8` | ≥ 1；≤ 64 |
| `memory.dialogue_episode_refresh_minutes` | integer | `90` | ≥ 5；≤ 1440 |
| `memory.max_dialogue_episodes` | integer | `12` | ≥ 1；≤ 32 |
| `memory.habit_learning_enabled` | boolean | `true` | 按领域规则校验 |
| `memory.food_menu_recommendation_enabled` | boolean | `true` | 按领域规则校验 |
| `memory.habit_min_count` | integer | `3` | ≥ 2；≤ 20 |
| `memory.habit_max_items` | integer | `24` | ≥ 8；≤ 80 |
| `memory.habit_refresh_minutes` | integer | `360` | ≥ 30；≤ 4320 |

### model.budget

生效范围：installation, role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.budget.enable_daily_token_soft_limit` | boolean | `false` | 按领域规则校验 |
| `model.budget.daily_token_soft_limit` | integer | `800000` | ≥ 0；≤ 1000000000000 |

### model.calendar.plan

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.calendar.plan.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.calendar.plan.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.calendar.plan.prompt` | text | `"沿原人格安排自己的生活；保留长期目标、当天小步和未完成事项，计划不是完成记录。"` | 按领域规则校验 |
| `model.calendar.plan.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.calendar.plan.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.calendar.plan.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.calendar.plan.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.calendar.plan.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.calendar.plan.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.conversation.context_image_caption

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.conversation.context_image_caption.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.context_image_caption.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.context_image_caption.prompt` | text | `"为已授权的群历史原图生成短小、谨慎的可见内容摘要。"` | 按领域规则校验 |
| `model.conversation.context_image_caption.max_output_tokens` | integer | `180` | ≥ 1；≤ 32768 |
| `model.conversation.context_image_caption.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.conversation.context_image_caption.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.conversation.context_image_caption.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.conversation.context_image_caption.timeout_seconds` | integer | `12` | ≥ 1；≤ 600 |
| `model.conversation.context_image_caption.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.conversation.image_narration

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.conversation.image_narration.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.image_narration.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.image_narration.prompt` | text | `"把本轮已授权图片转述为简短、谨慎、来源对应的文字。"` | 按领域规则校验 |
| `model.conversation.image_narration.max_output_tokens` | integer | `320` | ≥ 1；≤ 32768 |
| `model.conversation.image_narration.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.conversation.image_narration.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.conversation.image_narration.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.conversation.image_narration.timeout_seconds` | integer | `15` | ≥ 1；≤ 600 |
| `model.conversation.image_narration.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.conversation.poke_reply

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.conversation.poke_reply.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.poke_reply.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.poke_reply.prompt` | text | `"依据已配置角色身份回应当前戳一戳互动。"` | 按领域规则校验 |
| `model.conversation.poke_reply.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.conversation.poke_reply.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.conversation.poke_reply.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.conversation.poke_reply.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.conversation.poke_reply.timeout_seconds` | integer | `15` | ≥ 1；≤ 600 |
| `model.conversation.poke_reply.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.conversation.reply

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.conversation.reply.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.reply.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.conversation.reply.prompt` | text | `"保持原角色，只根据当前输入回复。"` | 按领域规则校验 |
| `model.conversation.reply.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.conversation.reply.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.conversation.reply.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.conversation.reply.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.conversation.reply.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.conversation.reply.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.image_review

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.image_review.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.image_review.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.image_review.prompt` | text | `"对群聊成图做可见内容安全分类，只返回固定 JSON 标签与置信度。"` | 按领域规则校验 |
| `model.image_review.max_output_tokens` | integer | `80` | ≥ 1；≤ 32768 |
| `model.image_review.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.image_review.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.image_review.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.image_review.timeout_seconds` | integer | `20` | ≥ 1；≤ 600 |
| `model.image_review.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.memory.reflect

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.memory.reflect.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.memory.reflect.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.memory.reflect.prompt` | text | `"按原人格整理已授权资料，有来源地更新认识，允许不修改。"` | 按领域规则校验 |
| `model.memory.reflect.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.memory.reflect.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.memory.reflect.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.memory.reflect.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.memory.reflect.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.memory.reflect.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.proactive.compose

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.proactive.compose.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.proactive.compose.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.proactive.compose.prompt` | text | `"保持原人格；基于真实来源决定是否主动联系，允许没有合适内容时不发送。"` | 按领域规则校验 |
| `model.proactive.compose.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.proactive.compose.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.proactive.compose.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.proactive.compose.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.proactive.compose.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.proactive.compose.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.proactive.judge

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.proactive.judge.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.proactive.judge.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.proactive.judge.prompt` | text | `"按当前人格与世界观点评一条已写好的主动消息，只决定放行或拦下。"` | 按领域规则校验 |
| `model.proactive.judge.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.proactive.judge.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.proactive.judge.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.proactive.judge.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.proactive.judge.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.proactive.judge.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.expression.contact_review

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.expression.contact_review.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.expression.contact_review.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.expression.contact_review.prompt` | text | `"检查本轮表达学习是否造成生硬或过度模仿。"` | 按领域规则校验 |
| `model.role.expression.contact_review.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.expression.contact_review.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.expression.contact_review.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.expression.contact_review.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.expression.contact_review.timeout_seconds` | integer | `8` | ≥ 1；≤ 600 |
| `model.role.expression.contact_review.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.expression.learn

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.expression.learn.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.expression.learn.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.expression.learn.prompt` | text | `"依据当前会话中已授权的文字，提出待审阅的可复用表达形式候选。"` | 按领域规则校验 |
| `model.role.expression.learn.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.expression.learn.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.expression.learn.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.expression.learn.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.expression.learn.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.expression.learn.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.expression.review

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.expression.review.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.expression.review.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.expression.review.prompt` | text | `"检查本轮表达学习是否造成生硬或过度模仿。"` | 按领域规则校验 |
| `model.role.expression.review.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.expression.review.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.expression.review.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.expression.review.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.expression.review.timeout_seconds` | integer | `8` | ≥ 1；≤ 600 |
| `model.role.expression.review.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.growth.progress

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.growth.progress.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.growth.progress.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.growth.progress.prompt` | text | `"依据已完成回执，为已确认目标提出待审阅的成长进展。"` | 按领域规则校验 |
| `model.role.growth.progress.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.growth.progress.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.growth.progress.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.growth.progress.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.growth.progress.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.growth.progress.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.journal.derive

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.journal.derive.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.derive.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.derive.prompt` | text | `"保持原人格，按本次私人书写任务及素材语义生成。"` | 按领域规则校验 |
| `model.role.journal.derive.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.journal.derive.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.journal.derive.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.journal.derive.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.journal.derive.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.journal.derive.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.journal.diary

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.journal.diary.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.diary.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.diary.prompt` | text | `"保持原人格，按本次私人书写任务及素材语义生成。"` | 按领域规则校验 |
| `model.role.journal.diary.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.journal.diary.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.journal.diary.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.journal.diary.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.journal.diary.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.journal.diary.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.journal.dream

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.journal.dream.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.dream.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.dream.prompt` | text | `"保持原人格，按本次私人书写任务及素材语义生成。"` | 按领域规则校验 |
| `model.role.journal.dream.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.journal.dream.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.journal.dream.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.journal.dream.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.journal.dream.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.journal.dream.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.journal.select

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.journal.select.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.select.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.journal.select.prompt` | text | `"保持原人格，按本次私人书写任务及素材语义生成。"` | 按领域规则校验 |
| `model.role.journal.select.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.journal.select.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.journal.select.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.journal.select.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.journal.select.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.journal.select.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.reading.consume

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.reading.consume.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.reading.consume.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.reading.consume.prompt` | text | `"保持原人格，阅读本次实际提供的原文片段。"` | 按领域规则校验 |
| `model.role.reading.consume.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.reading.consume.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.reading.consume.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.reading.consume.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.reading.consume.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.reading.consume.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.self_review

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.self_review.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.self_review.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.self_review.prompt` | text | `"依据角色自己的近期行为证据，提出待审阅的自我复盘指导候选。"` | 按领域规则校验 |
| `model.role.self_review.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.self_review.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.self_review.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.self_review.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.self_review.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.self_review.replacement_scope` | text | `"all"` | 按领域规则校验 |

### model.role.state.maintain

生效范围：installation, role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `model.role.state.maintain.provider` | text | `"native-model"` | 按领域规则校验 |
| `model.role.state.maintain.fallback` | text | `"native-model"` | 按领域规则校验 |
| `model.role.state.maintain.prompt` | text | `"保持原人格，维护自己的生活状态。"` | 按领域规则校验 |
| `model.role.state.maintain.max_output_tokens` | integer | `100` | ≥ 1；≤ 32768 |
| `model.role.state.maintain.replacement_rules` | text | `"[]"` | 按领域规则校验 |
| `model.role.state.maintain.fallback_on_refusal` | boolean | `false` | 按领域规则校验 |
| `model.role.state.maintain.refusal_terms` | text | `"很抱歉，我无法\n很抱歉,我无法\n我有我自己的底线\n我们可以聊聊别的\n我无法满足\n露骨性行为\n没办法提交这个请求\n这个请求没办法提交\nThe prompt could not be submitted\nrequest could not be submitted"` | 文本上限 4096 |
| `model.role.state.maintain.timeout_seconds` | integer | `60` | ≥ 1；≤ 600 |
| `model.role.state.maintain.replacement_scope` | text | `"all"` | 按领域规则校验 |

### person

生效范围：role, relationship。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `person.acquaintance_enabled` | boolean | `true` | 按领域规则校验 |
| `person.acquaintance_card_chars` | integer | `1024` | ≥ 256；≤ 4096 |
| `person.cross_window_awareness_enabled` | boolean | `true` | 按领域规则校验 |
| `person.cross_window_continuity_enabled` | boolean | `true` | 按领域规则校验 |
| `person.cross_window_continuity_minutes` | integer | `30` | ≥ 5；≤ 180 |
| `person.cross_window_private_group_hours` | integer | `12` | ≥ 1；≤ 48 |
| `person.cross_window_max_items` | integer | `4` | ≥ 1；≤ 8 |
| `person.cross_window_attention_minutes` | integer | `30` | ≥ 0；≤ 120 |
| `person.cross_window_attention_wait_seconds` | integer | `3` | ≥ 0；≤ 10 |
| `person.cross_window_group_identity_enabled` | boolean | `true` | 按领域规则校验 |
| `person.cross_window_peer_minutes` | integer | `5` | ≥ 1；≤ 60 |
| `person.cross_window_peer_reply_minutes` | integer | `60` | ≥ 1；≤ 720 |

### person.learning

生效范围：relationship。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `person.learning.acquaintance_learning_enabled` | boolean | `true` | 按领域规则校验 |

### photo.reference

生效范围：role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `photo.reference.enabled` | boolean | `false` | 按领域规则校验 |
| `photo.reference.group_enabled` | boolean | `false` | 按领域规则校验 |
| `photo.reference.daily_outfit_enabled` | boolean | `false` | 按领域规则校验 |
| `photo.reference.daily_outfit_rotation_days` | integer | `14` | ≥ 1；≤ 365 |

### private_access

生效范围：installation, role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `private_access.dialogue_default` | boolean | `true` | 按领域规则校验 |
| `private_access.proactive_default` | boolean | `false` | 按领域规则校验 |
| `private_access.denied_reply` | text | `"老大不让我和陌生人说话哦"` | 按领域规则校验 |
| `private_access.notice_cooldown_seconds` | integer | `21600` | ≥ 0；≤ 604800 |
| `private_access.stranger_notice_enabled` | boolean | `true` | 按领域规则校验 |
| `private_access.stranger_notice_daily_cap` | integer | `3` | ≥ 0；≤ 100 |

### proactive.contact

生效范围：installation, role, relationship, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `proactive.contact.enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.note` | text | `""` | 按领域规则校验 |
| `proactive.contact.style_prompt` | text | `""` | 按领域规则校验 |
| `proactive.contact.quiet_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.quiet_start` | text | `"23:00"` | 按领域规则校验 |
| `proactive.contact.quiet_end` | text | `"07:00"` | 按领域规则校验 |
| `proactive.contact.quiet_timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `proactive.contact.meal_checkin_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.meal_lunch_time` | text | `"12:00"` | 按领域规则校验 |
| `proactive.contact.meal_dinner_time` | text | `"18:00"` | 按领域规则校验 |
| `proactive.contact.date_checkin_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.date_checkin_time` | text | `"09:00"` | 按领域规则校验 |
| `proactive.contact.important_dates` | text | `"[]"` | 按领域规则校验 |
| `proactive.contact.weather_checkin_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.weather_checkin_time` | text | `"08:30"` | 按领域规则校验 |
| `proactive.contact.weather_change_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.official_weather_alert_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.news_share_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.news_source_kind` | text | `"host"` | 按领域规则校验 |
| `proactive.contact.news_source_uid` | text | `""` | 按领域规则校验 |
| `proactive.contact.news_source_url` | text | `""` | 按领域规则校验 |
| `proactive.contact.web_exploration_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.web_exploration_interests` | text | `""` | 按领域规则校验 |
| `proactive.contact.news_daily_hot_read_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.news_hot_sources` | text | `"weibo,hackernews"` | 按领域规则校验 |
| `proactive.contact.external_event_self_link_enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.official_alert_min_severity` | text | `""` | 按领域规则校验 |
| `proactive.contact.balance_awareness_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.balance_include_amount_in_message` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.voice_action_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.poke_action_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.dedup_enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.dedup_last_message_enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.dedup_policies` | text | `"semantic,content_fingerprint,life_event,event_revision"` | 按领域规则校验 |
| `proactive.contact.balance_currency_label` | text | `"元"` | 按领域规则校验 |
| `proactive.contact.enable_proactive_burst` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.proactive_intensity_preset` | text | `"off"` | 按领域规则校验 |
| `proactive.contact.proactive_hour_activity_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.proactive_hour_activity_curve` | text | `"0.22,0.16,0.12,0.10,0.10,0.14,0.28,0.50,0.66,0.72,0.78,0.92,1.00,0.94,0.82,0.74,0.78,0.92,1.00,0.98,0.88,0.70,0.48,0.32"` | 按领域规则校验 |
| `proactive.contact.enable_daily_greetings` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.allow_insomnia_night_message` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.greeting_morning_window` | text | `"07:45-10:20"` | 按领域规则校验 |
| `proactive.contact.greeting_noon_window` | text | `"12:05-13:35"` | 按领域规则校验 |
| `proactive.contact.greeting_evening_window` | text | `"20:10-21:20"` | 按领域规则校验 |
| `proactive.contact.insomnia_night_start` | text | `"23:00"` | 按领域规则校验 |
| `proactive.contact.insomnia_night_end` | text | `"06:00"` | 按领域规则校验 |
| `proactive.contact.insomnia_require_sleep_state` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.morning_chain_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.morning_role_greeting_enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.morning_nudge_enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.routine_learning_enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.wake_require_device_evidence` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.wake_morning_start` | text | `"05:00"` | 按领域规则校验 |
| `proactive.contact.wake_morning_end` | text | `"11:30"` | 按领域规则校验 |
| `proactive.contact.enable_llm_proactive_persona_judge` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.proactive_persona_judge_exempt_purposes` | text | `""` | 按领域规则校验 |
| `proactive.contact.expression_prompt` | text | `"像角色自然加入日常交流时发出的消息：结合 recent_timing、近期对话和角色当下状态判断是接续话头还是另起话题，保留人格的用词和关系距离。\n短时间内刚联系过时，不用郑重重开场、不强调刚想到对方或像隔了很久才见；可以顺着刚聊的内容说，也可以像随手发条消息那样带来一个具体的新念头或生活切片。围绕一个由头说…` | 按领域规则校验 |
| `proactive.contact.news_sharing_prompt` | text | `"把新闻当作看到值得分享的内容后想说的一段话。保持当前人格的年龄感、用词和关系距离，挑一个真正吸引你的亮点，说清发生了什么，再给一点具体感想或好奇，不改写成早报清单或缩短的新闻稿。\n事实只取本次标题和摘要；想象、疑问用主观语气，不补剧情、背景、数字或结论。轻松内容可以有惊喜，严肃、伤亡和风险消息按内容认真回应；…` | 按领域规则校验 |
| `proactive.contact.length_prompt` | text | `"这次主动正文按当前强度档位控制在 {chars} 字以内；把想说的意思和有内容的感想自然说完整，保留必要的解释和段落。无需压成一句，也不为凑长度补充内容。"` | 按领域规则校验 |
| `proactive.contact.news_length_prompt` | text | `"这次新闻分享的全部正文合计控制在 {chars} 字以内；挑一个亮点轻快地说清，保留有内容的感想和自然停顿，无需压成一句。不要为凑字数补充事实、话题或追问。"` | 按领域规则校验 |
| `proactive.contact.affection.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.affection.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.affection.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.care.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.care.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.care.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.play.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.play.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.play.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.repair.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.repair.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.repair.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.chat.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.chat.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.chat.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.greeting.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.greeting.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.greeting.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.life.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.life.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.life.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.creation.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.creation.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.creation.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.news.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.news.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.news.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.followup.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.followup.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.followup.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.invitation.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.invitation.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.invitation.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.reminder.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.reminder.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.reminder.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.environment.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.environment.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.environment.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.meal.enabled` | boolean | `true` | 按领域规则校验 |
| `proactive.contact.meal.weight` | weight | `1.0` | 按领域规则校验 |
| `proactive.contact.meal.pause_until` | text | `""` | 按领域规则校验 |
| `proactive.contact.automatic_enabled` | boolean | `false` | 按领域规则校验 |
| `proactive.contact.interval_seconds` | integer | `3600` | ≥ 60；≤ 604800 |
| `proactive.contact.idle_seconds` | integer | `900` | ≥ 0；≤ 86400 |
| `proactive.contact.unanswered_slowdown_start` | integer | `1` | ≥ 1；≤ 10 |
| `proactive.contact.unanswered_pause_after` | integer | `0` | ≥ 0；≤ 50 |
| `proactive.contact.dedup_sent_window_minutes` | integer | `240` | ≥ 0；≤ 1440 |
| `proactive.contact.dedup_last_message_window_minutes` | integer | `240` | ≥ 0；≤ 1440 |
| `proactive.contact.dedup_weather_window_minutes` | integer | `1080` | ≥ 0；≤ 2880 |
| `proactive.contact.dedup_min_shared_tokens` | integer | `1` | ≥ 1；≤ 4 |
| `proactive.contact.event_max_age_seconds` | integer | `3600` | ≥ 60；≤ 86400 |
| `proactive.contact.max_contacts_24h` | integer | `3` | ≥ 0；≤ 100 |
| `proactive.contact.balance_check_interval_minutes` | integer | `60` | ≥ 5；≤ 1440 |
| `proactive.contact.news_check_interval_minutes` | integer | `180` | ≥ 15；≤ 1440 |
| `proactive.contact.web_exploration_min_interval_hours` | integer | `8` | ≥ 1；≤ 168 |
| `proactive.contact.web_exploration_result_count` | integer | `8` | ≥ 1；≤ 30 |
| `proactive.contact.news_hot_result_count` | integer | `10` | ≥ 3；≤ 30 |
| `proactive.contact.external_event_self_link_cooldown_hours` | integer | `12` | ≥ 0；≤ 168 |
| `proactive.contact.contact_followup_after_minutes` | integer | `45` | ≥ 10；≤ 1440 |
| `proactive.contact.contact_followup_cooldown_minutes` | integer | `180` | ≥ 30；≤ 2880 |
| `proactive.contact.balance_message_cooldown_hours` | integer | `24` | ≥ 1；≤ 168 |
| `proactive.contact.important_date_lookahead_days` | integer | `0` | ≥ 0；≤ 30 |
| `proactive.contact.meal_care_followup_minutes` | integer | `45` | ≥ 1；≤ 240 |
| `proactive.contact.balance_low_threshold` | integer | `10` | ≥ 0；≤ 1000000000 |
| `proactive.contact.balance_critical_threshold` | integer | `3` | ≥ 0；≤ 1000000000 |
| `proactive.contact.balance_low_percent_threshold` | integer | `15` | ≥ 0；≤ 100 |
| `proactive.contact.balance_critical_percent_threshold` | integer | `5` | ≥ 0；≤ 100 |
| `proactive.contact.voice_action_max_chars` | integer | `30` | ≥ 6；≤ 80 |
| `proactive.contact.voice_action_cooldown_minutes` | integer | `60` | ≥ 0；≤ 1440 |
| `proactive.contact.poke_action_daily_limit` | integer | `1` | ≥ 0；≤ 20 |
| `proactive.contact.poke_action_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `proactive.contact.proactive_burst_max_messages` | integer | `2` | ≥ 2；≤ 3 |
| `proactive.contact.proactive_burst_gap_min_seconds` | integer | `45` | ≥ 10；≤ 600 |
| `proactive.contact.proactive_burst_gap_max_seconds` | integer | `180` | ≥ 10；≤ 900 |
| `proactive.contact.proactive_closing_grace_minutes` | integer | `45` | ≥ 0；≤ 240 |
| `proactive.contact.proactive_closing_contacts_threshold` | integer | `3` | ≥ 1；≤ 10 |
| `proactive.contact.proactive_intensity_body_chars` | integer | `0` | ≥ 0；≤ 2000 |
| `proactive.contact.greeting_idle_minutes` | integer | `30` | ≥ 0；≤ 240 |
| `proactive.contact.insomnia_night_daily_limit` | integer | `1` | ≥ 0；≤ 3 |
| `proactive.contact.proactive_share_probability` | integer | `100` | ≥ 0；≤ 100 |
| `proactive.contact.appointment_lead_minutes` | integer | `30` | ≥ 0；≤ 240 |
| `proactive.contact.appointment_lag_minutes` | integer | `0` | ≥ 0；≤ 180 |
| `proactive.contact.appointment_pre_silence_minutes` | integer | `20` | ≥ 0；≤ 240 |
| `proactive.contact.proactive_persona_judge_threshold` | integer | `62` | ≥ 0；≤ 100 |
| `proactive.contact.proactive_persona_judge_cache_minutes` | integer | `180` | ≥ 0；≤ 720 |
| `proactive.contact.morning_nudge_delay_minutes` | integer | `25` | ≥ 10；≤ 90 |
| `proactive.contact.morning_nudge_max_attempts` | integer | `1` | ≥ 0；≤ 2 |
| `proactive.contact.routine_window_days` | integer | `60` | ≥ 14；≤ 180 |
| `proactive.contact.wake_contact_window_minutes` | integer | `90` | ≥ 15；≤ 240 |
| `proactive.contact.wake_contact_min_confidence` | integer | `65` | ≥ 40；≤ 100 |
| `proactive.contact.wake_contact_max_daily` | integer | `1` | ≥ 0；≤ 3 |
| `proactive.contact.generation_history_limit` | integer | `8` | ≥ 0；≤ 64 |
| `proactive.contact.history_max_chars` | integer | `8192` | ≥ 0；≤ 8192 |
| `proactive.contact.official_alert_poll_minutes` | integer | `5` | ≥ 1；≤ 1440 |
| `proactive.contact.weather_sample_minutes` | integer | `60` | ≥ 10；≤ 1440 |
| `proactive.contact.unanswered_max_interval_multiplier` | weight | `2.2` | ≥ 1.0；≤ 8.0 |
| `proactive.contact.dedup_min_overlap_ratio` | probability | `0.0` | 按领域规则校验 |
| `proactive.contact.silence_min_confidence` | probability | `0.66` | 按领域规则校验 |
| `proactive.contact.silence_feedback_penalty` | probability | `0.2` | 按领域规则校验 |
| `proactive.contact.external_event_self_link_weight` | weight | `1.5` | ≥ 0.1；≤ 5.0 |
| `proactive.contact.morning_wake_confidence_floor` | probability | `0.25` | 按领域规则校验 |

### qzone

生效范围：window, role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `qzone.enabled` | boolean | `false` | 按领域规则校验 |
| `qzone.feed_recent_posts` | integer | `10` | ≥ 1；≤ 30 |
| `qzone.like_enabled` | boolean | `false` | 按领域规则校验 |
| `qzone.comment_enabled` | boolean | `false` | 按领域规则校验 |
| `qzone.publish_enabled` | boolean | `false` | 按领域规则校验 |
| `qzone.action_min_interval_minutes` | integer | `30` | ≥ 5；≤ 1440 |
| `qzone.max_actions_per_tick` | integer | `1` | ≥ 1；≤ 5 |
| `qzone.comment_recent_posts` | integer | `5` | ≥ 1；≤ 20 |
| `qzone.publish_max_daily` | integer | `1` | ≥ 1；≤ 10 |
| `qzone.topic_auto_enabled` | boolean | `false` | 按领域规则校验 |
| `qzone.topic_require_confirmation` | boolean | `true` | 按领域规则校验 |
| `qzone.topic_prompt_guidance` | text | `""` | 文本上限 4000 |
| `qzone.life_documentary_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.life_documentary_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.life_documentary_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.life_documentary_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.life_documentary_scenes` | text | `"conversation,role_activity,date_marker"` | 文本上限 512 |
| `qzone.emotion_reflection_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.emotion_reflection_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.emotion_reflection_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.emotion_reflection_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.emotion_reflection_scenes` | text | `"conversation,relationship,free_expression"` | 文本上限 512 |
| `qzone.interest_hobby_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.interest_hobby_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.interest_hobby_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.interest_hobby_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.interest_hobby_scenes` | text | `"conversation,external_material,role_activity"` | 文本上限 512 |
| `qzone.opinion_hot_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.opinion_hot_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.opinion_hot_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.opinion_hot_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.opinion_hot_scenes` | text | `"external_material,conversation"` | 文本上限 512 |
| `qzone.help_interaction_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.help_interaction_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.help_interaction_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.help_interaction_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.help_interaction_scenes` | text | `"conversation,agenda,external_material,relationship"` | 文本上限 512 |
| `qzone.ritual_memory_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.ritual_memory_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.ritual_memory_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.ritual_memory_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.ritual_memory_scenes` | text | `"date_marker,relationship,conversation"` | 文本上限 512 |
| `qzone.meaningless_status_enabled` | boolean | `true` | 按领域规则校验 |
| `qzone.meaningless_status_daily_max` | integer | `1` | ≥ 0；≤ 10 |
| `qzone.meaningless_status_cooldown_minutes` | integer | `30` | ≥ 0；≤ 1440 |
| `qzone.meaningless_status_min_confidence` | probability | `0.65` | 按领域规则校验 |
| `qzone.meaningless_status_scenes` | text | `"free_expression,conversation,role_activity"` | 文本上限 512 |

### relationship.profile

生效范围：relationship。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `relationship.profile.default_nickname` | text | `""` | 文本上限 100 |
| `relationship.profile.user_gender` | text | `""` | 文本上限 80 |
| `relationship.profile.user_birthday` | text | `""` | 文本上限 100 |
| `relationship.profile.user_occupation` | text | `""` | 文本上限 160 |
| `relationship.profile.role_relation` | text | `""` | 文本上限 240 |
| `relationship.profile.interaction` | text | `""` | 文本上限 900 |
| `relationship.profile.extra` | text | `""` | 文本上限 900 |

### role.growth

生效范围：window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `role.growth.read_enabled` | boolean | `false` | 按领域规则校验 |
| `role.growth.proposals_enabled` | boolean | `false` | 按领域规则校验 |

### role.growth.skills

生效范围：installation, role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `role.growth.skills.enabled` | boolean | `true` | 按领域规则校验 |
| `role.growth.skills.custom_skills` | text | `"[]"` | 按领域规则校验 |
| `role.growth.skills.schedule_influence_strength` | integer | `0` | ≥ 0；≤ 3 |

### role.life

生效范围：window, role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `role.life.enabled` | boolean | `false` | 按领域规则校验 |
| `role.life.diary_enabled` | boolean | `true` | 按领域规则校验 |
| `role.life.diary_time` | text | `"23:50"` | 按领域规则校验 |
| `role.life.timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `role.life.sleep_enabled` | boolean | `false` | 按领域规则校验 |
| `role.life.sleep_time` | text | `"00:30"` | 按领域规则校验 |
| `role.life.sleep_timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `role.life.sleep_variation_minutes` | integer | `20` | ≥ 0；≤ 120 |
| `role.life.sleep_window_minutes` | integer | `120` | ≥ 0；≤ 360 |
| `role.life.sleep_minutes` | integer | `480` | ≥ 1；≤ 1440 |
| `role.life.reading_enabled` | boolean | `false` | 按领域规则校验 |
| `role.life.derive_enabled` | boolean | `true` | 按领域规则校验 |
| `role.life.diary_style_prompt` | text | `""` | 按领域规则校验 |
| `role.life.dream_theme_candidates` | text | `""` | 按领域规则校验 |
| `role.life.dream_mixed_themes_enabled` | boolean | `false` | 按领域规则校验 |
| `role.life.dream_intimate_theme_enabled` | boolean | `false` | 按领域规则校验 |
| `role.life.dream_afterglow_mode` | text | `"auto"` | 按领域规则校验 |
| `role.life.enable_rest_reply_simulation` | boolean | `false` | 按领域规则校验 |
| `role.life.rest_reply_mode` | text | `"probability"` | 按领域规则校验 |
| `role.life.rest_reply_probability` | integer | `18` | ≥ 0；≤ 100 |
| `role.life.rest_reply_llm_threshold` | integer | `65` | ≥ 0；≤ 100 |
| `role.life.rest_reply_active_windows` | text | `"23:00-08:30,12:20-13:40"` | 按领域规则校验 |
| `role.life.rest_reply_awake_grace_minutes` | integer | `30` | ≥ 0；≤ 240 |
| `role.life.enable_rest_backlog_reply` | boolean | `true` | 按领域规则校验 |
| `role.life.rest_backlog_max_messages` | integer | `4` | ≥ 1；≤ 32 |

### role.profile

生效范围：role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `role.profile.name` | text | `""` | 按领域规则校验 |
| `role.profile.species` | text | `""` | 按领域规则校验 |
| `role.profile.birthday` | text | `""` | 按领域规则校验 |
| `role.profile.age` | text | `""` | 按领域规则校验 |
| `role.profile.gender` | text | `""` | 按领域规则校验 |
| `role.profile.occupation` | text | `""` | 按领域规则校验 |
| `role.profile.identity` | text | `""` | 按领域规则校验 |
| `role.profile.appearance_points` | text | `""` | 按领域规则校验 |
| `role.profile.hair` | text | `""` | 按领域规则校验 |
| `role.profile.eyes` | text | `""` | 按领域规则校验 |
| `role.profile.clothing` | text | `""` | 按领域规则校验 |
| `role.profile.image_identity_hint` | text | `""` | 按领域规则校验 |
| `role.profile.appearance` | text | `""` | 按领域规则校验 |
| `role.profile.personality` | text | `""` | 按领域规则校验 |
| `role.profile.first_person` | text | `""` | 按领域规则校验 |
| `role.profile.speech_style` | text | `""` | 按领域规则校验 |
| `role.profile.emotional_style` | text | `""` | 按领域规则校验 |
| `role.profile.social_distance` | text | `""` | 按领域规则校验 |
| `role.profile.reaction_patterns` | text | `""` | 按领域规则校验 |
| `role.profile.voice_examples` | text | `""` | 按领域规则校验 |
| `role.profile.signature_phrases` | text | `""` | 按领域规则校验 |
| `role.profile.daily_habits` | text | `""` | 按领域规则校验 |
| `role.profile.key_lore` | text | `""` | 按领域规则校验 |
| `role.profile.character_extra` | text | `""` | 按领域规则校验 |
| `role.profile.motivations` | text | `""` | 按领域规则校验 |
| `role.profile.core_values` | text | `""` | 按领域规则校验 |
| `role.profile.desire` | text | `""` | 按领域规则校验 |
| `role.profile.hobbies` | text | `""` | 按领域规则校验 |
| `role.profile.boundaries` | text | `""` | 按领域规则校验 |
| `role.profile.taboos` | text | `""` | 按领域规则校验 |
| `role.profile.world_name` | text | `""` | 按领域规则校验 |
| `role.profile.era` | text | `""` | 按领域规则校验 |
| `role.profile.tone` | text | `""` | 按领域规则校验 |
| `role.profile.rules` | text | `""` | 按领域规则校验 |
| `role.profile.scenes` | text | `""` | 按领域规则校验 |
| `role.profile.network` | text | `""` | 按领域规则校验 |
| `role.profile.world_extra` | text | `""` | 按领域规则校验 |
| `role.profile.world` | text | `""` | 按领域规则校验 |
| `role.profile.main_companion_subject` | text | `""` | 按领域规则校验 |
| `role.profile.expression_private_source_mode` | text | `"owner"` | 按领域规则校验 |
| `role.profile.expression_private_source_subject_ids` | text | `"[]"` | 按领域规则校验 |
| `role.profile.expression_private_application_mode` | text | `"all"` | 按领域规则校验 |
| `role.profile.expression_private_application_subject_ids` | text | `"[]"` | 按领域规则校验 |
| `role.profile.avatar_data_url` | text | `""` | 按领域规则校验 |

### role.state

生效范围：role, window。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `role.state.enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.maintenance_minutes` | integer | `30` | ≥ 1；≤ 1440 |
| `role.state.hunger_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.health_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.cycle_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.calendar_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.energy_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.sleep_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.busy_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.location_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.energy_expression_prompt` | text | `""` | 按领域规则校验 |
| `role.state.hunger_expression_prompt` | text | `""` | 按领域规则校验 |
| `role.state.health_expression_prompt` | text | `""` | 按领域规则校验 |
| `role.state.home_show_energy` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_health` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_hunger` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_sleep` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_cycle` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_busy` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_location` | boolean | `true` | 按领域规则校验 |
| `role.state.home_show_mood` | boolean | `true` | 按领域规则校验 |
| `role.state.home_only_special_health` | boolean | `false` | 按领域规则校验 |
| `role.state.home_only_special_hunger` | boolean | `false` | 按领域规则校验 |
| `role.state.home_only_special_sleep` | boolean | `false` | 按领域规则校验 |
| `role.state.home_only_special_cycle` | boolean | `false` | 按领域规则校验 |
| `role.state.home_only_special_busy` | boolean | `false` | 按领域规则校验 |
| `role.state.typing_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.typing_refresh_seconds` | integer | `4` | ≥ 1；≤ 10 |
| `role.state.presence_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.online_status_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.mood_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.mood_cross_window` | boolean | `true` | 按领域规则校验 |
| `role.state.mood_update_probability` | probability | `0.6` | 按领域规则校验 |
| `role.state.mood_interest_window_minutes` | integer | `120` | ≥ 5；≤ 1440 |
| `role.state.mood_update_max_delta` | integer | `2` | ≥ 1；≤ 4 |
| `role.state.mood_decay_half_life_minutes` | integer | `90` | ≥ 5；≤ 1440 |
| `role.state.mood_neutral_band` | integer | `3` | ≥ 1；≤ 4 |
| `role.state.humanized_state_intensity` | integer | `50` | ≥ 0；≤ 100 |
| `role.state.daily_state_patrol_enabled` | boolean | `true` | 按领域规则校验 |
| `role.state.daily_state_patrol_time` | text | `"04:00"` | 按领域规则校验 |
| `role.state.daily_state_patrol_retention_days` | integer | `30` | ≥ 3；≤ 180 |
| `role.state.cycle_mode` | text | `"basic"` | 按领域规则校验 |
| `role.state.cycle_timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `role.state.cycle_menstrual_days` | integer | `5` | ≥ 1；≤ 30 |
| `role.state.cycle_follicular_days` | integer | `7` | ≥ 1；≤ 30 |
| `role.state.cycle_pre_ovulation_days` | integer | `2` | ≥ 1；≤ 30 |
| `role.state.cycle_ovulation_days` | integer | `2` | ≥ 1；≤ 30 |
| `role.state.cycle_luteal_days` | integer | `9` | ≥ 1；≤ 30 |
| `role.state.cycle_pms_days` | integer | `3` | ≥ 1；≤ 30 |
| `role.state.cycle_discomfort_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.cycle_discomfort_chance` | integer | `55` | ≥ 0；≤ 100 |
| `role.state.cycle_discomfort_types` | text | `"痛经,头痛,腰酸,乏力"` | 按领域规则校验 |
| `role.state.cycle_link_intensity` | boolean | `false` | 按领域规则校验 |
| `role.state.cycle_expression_prompt` | text | `""` | 按领域规则校验 |
| `role.state.cycle_initialization` | text | `"natural"` | 按领域规则校验 |
| `role.state.cycle_variation_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.cycle_menstrual_energy` | integer | `-12` | ≥ -50；≤ 30 |
| `role.state.cycle_menstrual_mood` | text | `"疲惫"` | 按领域规则校验 |
| `role.state.cycle_menstrual_prompt` | text | `"处于月经期，身体更容易疲倦，情绪感受稍敏锐"` | 按领域规则校验 |
| `role.state.cycle_follicular_energy` | integer | `0` | ≥ -50；≤ 30 |
| `role.state.cycle_follicular_mood` | text | `"轻快"` | 按领域规则校验 |
| `role.state.cycle_follicular_prompt` | text | `"处于卵泡期，精力平稳回升，心情逐渐轻快"` | 按领域规则校验 |
| `role.state.cycle_pre_ovulation_energy` | integer | `8` | ≥ -50；≤ 30 |
| `role.state.cycle_pre_ovulation_mood` | text | `"期待"` | 按领域规则校验 |
| `role.state.cycle_pre_ovulation_prompt` | text | `"处于排卵前期，身体逐渐轻盈，精力有所上升"` | 按领域规则校验 |
| `role.state.cycle_ovulation_energy` | integer | `9` | ≥ -50；≤ 30 |
| `role.state.cycle_ovulation_mood` | text | `"明朗"` | 按领域规则校验 |
| `role.state.cycle_ovulation_prompt` | text | `"处于排卵期，精力较充足，社交意愿稍有增强"` | 按领域规则校验 |
| `role.state.cycle_luteal_energy` | integer | `5` | ≥ -50；≤ 30 |
| `role.state.cycle_luteal_mood` | text | `"平稳"` | 按领域规则校验 |
| `role.state.cycle_luteal_prompt` | text | `"处于黄体期，精力尚可，情绪整体平稳"` | 按领域规则校验 |
| `role.state.cycle_pms_energy` | integer | `-8` | ≥ -50；≤ 30 |
| `role.state.cycle_pms_mood` | text | `"敏感"` | 按领域规则校验 |
| `role.state.cycle_pms_prompt` | text | `"处于 PMS 期，精力有所下降，情绪波动稍明显"` | 按领域规则校验 |
| `role.state.schedule_simulation_mode` | text | `"orchestrated"` | 按领域规则校验 |
| `role.state.planning_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.planning_timezone` | text | `"Asia/Shanghai"` | 按领域规则校验 |
| `role.state.planning_horizon_days` | integer | `90` | ≥ 1；≤ 366 |
| `role.state.planning_refine_minutes` | integer | `15` | ≥ 1；≤ 1440 |
| `role.state.planning_max_items` | integer | `12` | ≥ 1；≤ 32 |
| `role.state.planning_prompt` | text | `""` | 按领域规则校验 |
| `role.state.planning_annual_calendars` | text | `""` | 按领域规则校验 |
| `role.state.planning_weather_enabled` | boolean | `false` | 按领域规则校验 |
| `role.state.planning_weather_location` | text | `""` | 按领域规则校验 |
| `role.state.planning_weather_max_age_minutes` | integer | `120` | ≥ 5；≤ 120 |

### wardrobe

生效范围：role。

| 字段 | 类型 | 默认值 | 取值边界 |
| --- | --- | --- | --- |
| `wardrobe.enabled` | boolean | `false` | 按领域规则校验 |
| `wardrobe.tendency` | text | `""` | ≤ 800 |
| `wardrobe.prompt_enabled` | boolean | `false` | 按领域规则校验 |
| `wardrobe.prompt_max_items` | integer | `12` | ≥ 1；≤ 24 |
| `wardrobe.image_max_count` | integer | `3` | ≥ 1；≤ 8 |
| `wardrobe.image_prompt` | text | `""` | ≤ 800 |
