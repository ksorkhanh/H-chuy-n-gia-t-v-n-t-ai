-- ============================================================
-- Legal Expert System - Seed Data
-- Vietnamese Land Law 2024 sample data
-- ============================================================

-- ============================================================
-- 1. Default Users (password = '123456' for all)
-- ============================================================
-- Password hash for '123456' with salt 'default_salt_admin'
INSERT INTO users (username, password_hash, salt, role, full_name, email) VALUES
('admin', 'ca6bbfc6063ae623cbba4dc7c3ee5d866a51a5774ac98979964a8e8b594102ad', 'default_salt_admin', 'admin', 'Quản trị viên', 'admin@legal.vn'),
('staff01', '7cedeb1bb94fbfa8c9c0f9aadf7fd183c8793d46e1842aa711b080b0b7a7c3a1', 'default_salt_staff', 'staff', 'Nguyễn Văn A', 'staff01@legal.vn'),
('expert01', '02351f85713eb01f1b148b76b14d0fc787cccf4bcd37f48d3abd9955b4791240', 'default_salt_expert', 'expert', 'TS. Trần Thị B', 'expert01@legal.vn');

-- ============================================================
-- 2. Permissions
-- ============================================================
INSERT INTO permissions (name, description) VALUES
('manage_legal', 'Quản lý văn bản pháp lý'),
('manage_rules', 'Quản lý luật suy diễn'),
('manage_users', 'Quản lý người dùng'),
('run_consultation', 'Thực hiện tư vấn'),
('view_results', 'Xem kết quả tư vấn'),
('view_history', 'Xem lịch sử tư vấn'),
('import_export', 'Import/Export dữ liệu'),
('propose_rules', 'Đề xuất luật mới');

-- Admin permissions
INSERT INTO role_permissions (role, permission_id) VALUES
('admin', 1), ('admin', 2), ('admin', 3), ('admin', 4),
('admin', 5), ('admin', 6), ('admin', 7);

-- Staff permissions
INSERT INTO role_permissions (role, permission_id) VALUES
('staff', 4), ('staff', 5), ('staff', 6);

-- Expert permissions
INSERT INTO role_permissions (role, permission_id) VALUES
('expert', 4), ('expert', 5), ('expert', 6), ('expert', 8), ('expert', 2);

-- ============================================================
-- 3. Legal Documents
-- ============================================================
INSERT INTO legal_documents (title, code, year, domain, description) VALUES
('Luật Đất đai 2024', 'LUAT_DD_2024', 2024, 'dat_dai', 'Luật Đất đai số 31/2024/QH15 được Quốc hội thông qua ngày 18/01/2024, có hiệu lực từ 01/01/2025'),
('Nghị định 88/2024/NĐ-CP', 'ND_88_2024', 2024, 'dat_dai', 'Nghị định quy định về bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất'),
('Nghị định 91/2019/NĐ-CP', 'ND_91_2019', 2019, 'dat_dai', 'Nghị định về xử phạt vi phạm hành chính trong lĩnh vực đất đai'),
('Luật Công chứng 2014', 'LUAT_CC_2014', 2014, 'dat_dai', 'Luật Công chứng số 53/2014/QH13 quy định về công chứng hợp đồng, giao dịch');

-- ============================================================
-- 4. Legal Articles - Module: Chuyển nhượng (transfer)
-- ============================================================
INSERT INTO legal_articles (document_id, article_number, clause, content, keywords) VALUES
-- Luật Đất đai 2024
(1, 'Điều 45', 'Khoản 1', 'Người sử dụng đất được thực hiện quyền chuyển nhượng quyền sử dụng đất khi có Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất; đất không có tranh chấp; quyền sử dụng đất không bị kê biên để bảo đảm thi hành án; trong thời hạn sử dụng đất.', 'chuyển nhượng, giấy chứng nhận, điều kiện, tranh chấp'),
(1, 'Điều 45', 'Khoản 2', 'Ngoài các điều kiện quy định tại khoản 1 Điều này, người sử dụng đất khi thực hiện các quyền chuyển nhượng phải đáp ứng các điều kiện theo quy định tại các điều từ Điều 46 đến Điều 50 của Luật này.', 'chuyển nhượng, điều kiện bổ sung'),
(1, 'Điều 27', NULL, 'Nhà nước công nhận quyền sử dụng đất thông qua việc cấp Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất cho người đang sử dụng đất ổn định.', 'giấy chứng nhận, công nhận, quyền sử dụng đất'),
(1, 'Điều 153', NULL, 'Hợp đồng chuyển nhượng quyền sử dụng đất phải được công chứng hoặc chứng thực, trừ trường hợp một bên là tổ chức kinh doanh bất động sản.', 'hợp đồng, công chứng, chứng thực, chuyển nhượng'),
(1, 'Điều 155', NULL, 'Người chuyển nhượng quyền sử dụng đất phải thực hiện nghĩa vụ tài chính gồm thuế thu nhập cá nhân, phí, lệ phí theo quy định của pháp luật.', 'nghĩa vụ tài chính, thuế, phí, lệ phí');

-- ============================================================
-- 5. Legal Articles - Module: Bồi thường (compensation)
-- ============================================================
INSERT INTO legal_articles (document_id, article_number, clause, content, keywords) VALUES
(1, 'Điều 79', 'Khoản 1', 'Nhà nước thu hồi đất trong các trường hợp: Để thực hiện dự án phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng; Để thực hiện các dự án tạo quỹ đất theo quy hoạch.', 'thu hồi đất, lợi ích quốc gia, phát triển kinh tế'),
(1, 'Điều 91', NULL, 'Nguyên tắc bồi thường khi Nhà nước thu hồi đất: Bồi thường bằng đất có cùng mục đích sử dụng hoặc bằng tiền theo giá đất cụ thể tại thời điểm có quyết định thu hồi đất.', 'bồi thường, nguyên tắc, giá đất, thu hồi'),
(1, 'Điều 95', NULL, 'Điều kiện được bồi thường về đất khi Nhà nước thu hồi đất: có Giấy chứng nhận hoặc đủ điều kiện cấp Giấy chứng nhận; đất không thuộc trường hợp giao không thu tiền sử dụng đất.', 'điều kiện bồi thường, giấy chứng nhận'),
(2, 'Điều 5', NULL, 'Giá đất cụ thể để tính bồi thường khi Nhà nước thu hồi đất được xác định theo phương pháp định giá đất quy định tại Luật Đất đai, phù hợp với giá đất phổ biến trên thị trường.', 'giá đất cụ thể, bồi thường, phương pháp định giá'),
(2, 'Điều 15', NULL, 'Hỗ trợ tái định cư: Hộ gia đình, cá nhân khi Nhà nước thu hồi đất ở mà phải di chuyển chỗ ở, nếu không có chỗ ở nào khác trong địa bàn xã, phường, thị trấn nơi có đất thu hồi thì được bố trí tái định cư.', 'hỗ trợ, tái định cư, thu hồi đất ở');

-- ============================================================
-- 6. Legal Articles - Module: Vi phạm (violation)
-- ============================================================
INSERT INTO legal_articles (document_id, article_number, clause, content, keywords) VALUES
(3, 'Điều 9', NULL, 'Sử dụng đất lấn, chiếm: Phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng đối với trường hợp lấn, chiếm đất chưa sử dụng có diện tích dưới 0,02 hecta tại khu vực nông thôn.', 'lấn chiếm, phạt tiền, đất chưa sử dụng, nông thôn'),
(3, 'Điều 10', NULL, 'Sử dụng đất không đúng mục đích: Phạt tiền từ 2.000.000 đồng đến 5.000.000 đồng khi chuyển mục đích sử dụng đất trồng lúa sang đất trồng cây lâu năm mà không được phép.', 'không đúng mục đích, chuyển mục đích, đất trồng lúa'),
(3, 'Điều 14', NULL, 'Tự ý chuyển nhượng quyền sử dụng đất dưới hình thức phân lô, bán nền mà không đủ điều kiện theo quy định: Phạt tiền từ 20.000.000 đồng đến 50.000.000 đồng.', 'phân lô bán nền, chuyển nhượng trái phép'),
(3, 'Điều 6', 'Khoản 1', 'Tình tiết tăng nặng: Vi phạm nhiều lần; tái phạm; vi phạm với diện tích lớn; gây hậu quả nghiêm trọng; không chấp hành quyết định xử phạt.', 'tăng nặng, tái phạm, hậu quả nghiêm trọng'),
(3, 'Điều 7', NULL, 'Biện pháp khắc phục hậu quả: Buộc khôi phục lại tình trạng ban đầu của đất trước khi vi phạm; buộc nộp lại số lợi bất hợp pháp có được do thực hiện hành vi vi phạm.', 'khắc phục, khôi phục, nộp lại, lợi bất hợp pháp');

-- ============================================================
-- 7. Legal Relations
-- ============================================================
INSERT INTO legal_relations (source_article_id, related_article_id, relation_type) VALUES
(1, 2, 'supplement'),    -- Điều 45 K1 <-> K2
(1, 3, 'reference'),     -- Điều 45 -> Điều 27 (giấy CN)
(1, 4, 'reference'),     -- Điều 45 -> Điều 153 (công chứng)
(4, 5, 'supplement'),    -- Điều 153 -> Điều 155 (nghĩa vụ TC)
(6, 7, 'detail'),        -- Điều 79 -> Điều 91 (nguyên tắc BT)
(7, 8, 'supplement'),    -- Điều 91 -> Điều 95 (điều kiện BT)
(7, 9, 'detail'),        -- Điều 91 -> NĐ88 Điều 5 (giá đất)
(8, 10, 'supplement');   -- Điều 95 -> NĐ88 Điều 15 (tái định cư)

-- ============================================================
-- 8. Fuzzy Rules - Module: Transfer (Chuyển nhượng QSD đất)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
-- Nếu tính pháp lý tốt VÀ giá trị phù hợp → Khả thi cao
('transfer', 'R1_Transfer_High', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"reasonable"}]', 'high_feasibility', 1.0, 1, 'Giấy tờ đầy đủ, giá hợp lý → Khả thi cao'),
('transfer', 'R2_Transfer_High2', '[{"variable":"legal_status","term":"complete"},{"variable":"area","term":"medium"},{"variable":"financial_obligation","term":"fulfilled"}]', 'high_feasibility', 0.9, 4, 'Pháp lý đầy đủ, diện tích vừa, đã nộp thuế → Khả thi cao'),
-- Nếu tính pháp lý trung bình → Khả thi trung bình
('transfer', 'R3_Transfer_Medium', '[{"variable":"legal_status","term":"partial"},{"variable":"land_value","term":"reasonable"}]', 'medium_feasibility', 0.8, 2, 'Giấy tờ chưa đầy đủ, giá hợp lý → Cần bổ sung hồ sơ'),
('transfer', 'R4_Transfer_Medium2', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"high"},{"variable":"location","term":"rural"}]', 'medium_feasibility', 0.7, 5, 'Pháp lý đầy đủ nhưng giá cao, vùng nông thôn → Cân nhắc'),
-- Nếu pháp lý kém → Khả thi thấp
('transfer', 'R5_Transfer_Low', '[{"variable":"legal_status","term":"incomplete"},{"variable":"land_value","term":"high"}]', 'low_feasibility', 1.0, 1, 'Không đủ giấy tờ → Không thể chuyển nhượng'),
('transfer', 'R6_Transfer_Low2', '[{"variable":"legal_status","term":"incomplete"},{"variable":"financial_obligation","term":"unfulfilled"}]', 'low_feasibility', 0.9, 5, 'Thiếu pháp lý và chưa nộp thuế → Rủi ro cao'),
-- Bổ sung luật cho Transfer
('transfer', 'R7_Transfer_Urban_High', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"high"},{"variable":"location","term":"urban"},{"variable":"financial_obligation","term":"fulfilled"}]', 'high_feasibility', 0.95, 1, 'Pháp lý đầy đủ, vị trí đô thị, tài chính xong → Khả thi rất cao'),
('transfer', 'R8_Transfer_Rural_Risk', '[{"variable":"legal_status","term":"partial"},{"variable":"land_value","term":"low"},{"variable":"location","term":"rural"},{"variable":"financial_obligation","term":"unfulfilled"}]', 'low_feasibility', 0.85, 5, 'Pháp lý chưa xong, vùng sâu, chưa nộp thuế → Rủi ro cao'),
('transfer', 'R9_Transfer_Suburban_Large', '[{"variable":"legal_status","term":"complete"},{"variable":"area","term":"large"},{"variable":"financial_obligation","term":"fulfilled"},{"variable":"location","term":"suburban"}]', 'high_feasibility', 0.9, 4, 'Diện tích lớn, ven đô, pháp lý và tài chính tốt → Khả thi cao'),
('transfer', 'R10_Transfer_Medium_Complex', '[{"variable":"legal_status","term":"partial"},{"variable":"land_value","term":"reasonable"},{"variable":"financial_obligation","term":"partial"},{"variable":"area","term":"medium"}]', 'medium_feasibility', 0.8, 2, 'Các yếu tố ở mức trung bình → Cần hoàn thiện thêm hồ sơ'),
('transfer', 'R11_Transfer_Urban_Small', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"high"},{"variable":"area","term":"small"},{"variable":"location","term":"urban"}]', 'medium_feasibility', 0.75, 1, 'Đất đô thị giá cao nhưng diện tích nhỏ → Khả thi vừa'),
('transfer', 'R12_Transfer_Large_Incomplete', '[{"variable":"legal_status","term":"incomplete"},{"variable":"land_value","term":"low"},{"variable":"financial_obligation","term":"fulfilled"},{"variable":"area","term":"large"}]', 'low_feasibility', 0.9, 5, 'Diện tích lớn nhưng pháp lý chưa ổn → Rủi ro pháp lý cao'),
('transfer', 'R13_Transfer_Suburban_Fulfilled', '[{"variable":"legal_status","term":"partial"},{"variable":"land_value","term":"reasonable"},{"variable":"location","term":"suburban"},{"variable":"financial_obligation","term":"fulfilled"}]', 'medium_feasibility', 0.85, 2, 'Ven đô, tài chính xong, pháp lý cần bổ sung → Khả thi trung bình'),
('transfer', 'R14_Transfer_Partial_Urban', '[{"variable":"legal_status","term":"partial"},{"variable":"financial_obligation","term":"partial"},{"variable":"location","term":"urban"}]', 'medium_feasibility', 0.7, 2, 'Pháp lý và tài chính chưa hoàn chỉnh ở đô thị → Khả thi trung bình'),
('transfer', 'R15_Transfer_Rural_Cheap', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"low"},{"variable":"area","term":"small"},{"variable":"location","term":"rural"}]', 'high_feasibility', 0.8, 1, 'Đất nông thôn nhỏ, rẻ, pháp lý đủ → Khả thi cao'),
('transfer', 'R16_Transfer_Incomplete_Rural', '[{"variable":"legal_status","term":"incomplete"},{"variable":"area","term":"small"},{"variable":"location","term":"rural"}]', 'low_feasibility', 1.0, 5, 'Đất nông thôn thiếu pháp lý → Rủi ro cao'),
('transfer', 'R17_Transfer_HighValue_Unpaid', '[{"variable":"legal_status","term":"complete"},{"variable":"financial_obligation","term":"unfulfilled"},{"variable":"land_value","term":"high"}]', 'medium_feasibility', 0.6, 5, 'Pháp lý đủ nhưng giá cao và chưa nộp thuế → Cần xử lý tài chính'),
('transfer', 'R18_Transfer_Large_Urban_Partial', '[{"variable":"legal_status","term":"partial"},{"variable":"area","term":"large"},{"variable":"location","term":"urban"},{"variable":"financial_obligation","term":"fulfilled"}]', 'medium_feasibility', 0.85, 2, 'Diện tích lớn ở đô thị, tài chính xong nhưng thiếu giấy tờ → Khả thi khá'),
('transfer', 'R19_Transfer_Urban_Incomplete', '[{"variable":"legal_status","term":"incomplete"},{"variable":"location","term":"urban"},{"variable":"land_value","term":"reasonable"}]', 'low_feasibility', 0.95, 5, 'Đất đô thị thiếu pháp lý → Không khả thi'),
('transfer', 'R20_Transfer_Small_Cheap_Partial', '[{"variable":"legal_status","term":"partial"},{"variable":"land_value","term":"low"},{"variable":"financial_obligation","term":"partial"},{"variable":"area","term":"small"}]', 'low_feasibility', 0.65, 2, 'Diện tích nhỏ, rẻ, thiếu nhiều điều kiện → Khả thi thấp');

-- ============================================================
-- 9. Fuzzy Rules - Module: Compensation (Bồi thường thu hồi đất)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
-- Bồi thường cao
('compensation', 'R1_Comp_High', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"long"},{"variable":"area","term":"large"}]', 'high_compensation', 1.0, 7, 'Đất ở, sử dụng lâu, diện tích lớn → Bồi thường cao'),
('compensation', 'R2_Comp_High2', '[{"variable":"land_type","term":"residential"},{"variable":"k_coefficient","term":"high"},{"variable":"resettlement","term":"needed"}]', 'high_compensation', 0.9, 10, 'Đất ở, hệ số K cao, cần tái định cư → Bồi thường cao'),
-- Bồi thường trung bình
('compensation', 'R3_Comp_Medium', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"medium"},{"variable":"area","term":"medium"}]', 'medium_compensation', 0.8, 8, 'Đất nông nghiệp, sử dụng trung bình → Bồi thường vừa'),
('compensation', 'R4_Comp_Medium2', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"short"},{"variable":"k_coefficient","term":"medium"}]', 'medium_compensation', 0.7, 9, 'Đất ở, mới sử dụng, hệ số K trung bình'),
-- Bồi thường thấp
('compensation', 'R5_Comp_Low', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"short"},{"variable":"area","term":"small"}]', 'low_compensation', 1.0, 8, 'Đất nông nghiệp, sử dụng ngắn, diện tích nhỏ → Bồi thường thấp'),
('compensation', 'R6_Comp_Low2', '[{"variable":"land_type","term":"unused"},{"variable":"usage_duration","term":"short"}]', 'low_compensation', 0.9, 6, 'Đất chưa sử dụng, thời gian ngắn → Bồi thường thấp'),
-- Bổ sung luật cho Compensation
('compensation', 'R7_Comp_Full_Support', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"long"},{"variable":"area","term":"large"},{"variable":"k_coefficient","term":"high"},{"variable":"resettlement","term":"needed"}]', 'high_compensation', 1.0, 10, 'Đất ở lâu năm, diện tích lớn, hệ số K cao, cần tái định cư → Bồi thường tối đa'),
('compensation', 'R8_Comp_Agri_Large', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"long"},{"variable":"area","term":"large"},{"variable":"k_coefficient","term":"medium"}]', 'medium_compensation', 0.9, 8, 'Đất nông nghiệp sử dụng lâu, diện tích lớn → Bồi thường khá'),
('compensation', 'R9_Comp_Res_Short_K_High', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"short"},{"variable":"area","term":"medium"},{"variable":"k_coefficient","term":"high"}]', 'medium_compensation', 0.85, 9, 'Đất ở mới sử dụng nhưng ở vị trí đắc địa (K cao) → Bồi thường trung bình'),
('compensation', 'R10_Comp_Unused_Small', '[{"variable":"land_type","term":"unused"},{"variable":"usage_duration","term":"medium"},{"variable":"area","term":"small"},{"variable":"k_coefficient","term":"low"}]', 'low_compensation', 0.9, 6, 'Đất chưa sử dụng, diện tích nhỏ, vị trí kém → Bồi thường thấp'),
('compensation', 'R11_Comp_Res_Needed', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"long"},{"variable":"area","term":"small"},{"variable":"resettlement","term":"needed"}]', 'high_compensation', 0.95, 10, 'Đất ở lâu năm dù diện tích nhỏ nhưng cần tái định cư → Ưu tiên bồi thường cao'),
('compensation', 'R12_Comp_Agri_K_High', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"medium"},{"variable":"area","term":"small"},{"variable":"k_coefficient","term":"high"}]', 'medium_compensation', 0.8, 9, 'Đất nông nghiệp diện tích nhỏ nhưng ở khu vực giá trị tăng cao → Bồi thường vừa'),
('compensation', 'R13_Comp_Res_Med_Large', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"medium"},{"variable":"k_coefficient","term":"low"},{"variable":"area","term":"large"}]', 'medium_compensation', 0.75, 9, 'Đất ở diện tích lớn nhưng hệ số K thấp → Bồi thường trung bình'),
('compensation', 'R14_Comp_Agri_Resettlement', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"long"},{"variable":"resettlement","term":"needed"}]', 'medium_compensation', 0.85, 8, 'Đất nông nghiệp lâu năm cần tái định cư → Bồi thường khá'),
('compensation', 'R15_Comp_Unused_Large', '[{"variable":"land_type","term":"unused"},{"variable":"usage_duration","term":"long"},{"variable":"area","term":"large"}]', 'medium_compensation', 0.65, 6, 'Đất chưa sử dụng nhưng diện tích lớn và lâu năm → Bồi thường vừa'),
('compensation', 'R16_Comp_Res_Short_Small', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"short"},{"variable":"area","term":"small"},{"variable":"k_coefficient","term":"low"}]', 'low_compensation', 0.8, 9, 'Đất ở nhỏ, mới sử dụng, vị trí kém → Bồi thường thấp'),
('compensation', 'R17_Comp_Agri_High_K', '[{"variable":"land_type","term":"agricultural"},{"variable":"k_coefficient","term":"high"},{"variable":"area","term":"large"}]', 'high_compensation', 0.7, 8, 'Đất nông nghiệp diện tích lớn ở vị trí đắc địa → Bồi thường cao'),
('compensation', 'R18_Comp_Unused_Resettlement', '[{"variable":"land_type","term":"unused"},{"variable":"resettlement","term":"needed"}]', 'low_compensation', 0.5, 6, 'Đất chưa sử dụng nhưng cần chỗ ở → Hỗ trợ mức thấp'),
('compensation', 'R19_Comp_Res_Med_K', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"long"},{"variable":"k_coefficient","term":"medium"},{"variable":"area","term":"medium"}]', 'high_compensation', 0.8, 7, 'Đất ở lâu năm, các yếu tố khác trung bình → Bồi thường cao'),
('compensation', 'R20_Comp_Agri_Short_Large', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"short"},{"variable":"k_coefficient","term":"low"},{"variable":"area","term":"large"}]', 'low_compensation', 0.9, 8, 'Đất nông nghiệp mới sử dụng, vị trí kém dù diện tích lớn → Bồi thường thấp');

-- ============================================================
-- 10. Fuzzy Rules - Module: Violation (Vi phạm hành chính đất đai)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
-- Mức xử phạt nặng
('violation', 'R1_Viol_Heavy', '[{"variable":"severity","term":"serious"},{"variable":"violation_area","term":"large"},{"variable":"recidivism","term":"yes"}]', 'heavy_penalty', 1.0, 14, 'Vi phạm nghiêm trọng, diện tích lớn, tái phạm → Phạt nặng'),
('violation', 'R2_Viol_Heavy2', '[{"variable":"severity","term":"serious"},{"variable":"damage","term":"high"}]', 'heavy_penalty', 0.9, 15, 'Vi phạm nghiêm trọng, thiệt hại lớn → Phạt nặng + khắc phục'),
-- Mức xử phạt trung bình
('violation', 'R3_Viol_Medium', '[{"variable":"severity","term":"moderate"},{"variable":"violation_area","term":"medium"},{"variable":"recidivism","term":"no"}]', 'medium_penalty', 0.8, 11, 'Vi phạm vừa, diện tích vừa, lần đầu → Phạt trung bình'),
('violation', 'R4_Viol_Medium2', '[{"variable":"severity","term":"moderate"},{"variable":"duration","term":"medium"},{"variable":"damage","term":"medium"}]', 'medium_penalty', 0.7, 12, 'Vi phạm vừa, thời gian vừa → Phạt trung bình'),
-- Mức xử phạt nhẹ
('violation', 'R5_Viol_Light', '[{"variable":"severity","term":"minor"},{"variable":"violation_area","term":"small"},{"variable":"recidivism","term":"no"}]', 'light_penalty', 1.0, 11, 'Vi phạm nhẹ, diện tích nhỏ, lần đầu → Phạt nhẹ/cảnh cáo'),
('violation', 'R6_Viol_Light2', '[{"variable":"severity","term":"minor"},{"variable":"damage","term":"low"}]', 'light_penalty', 0.9, 12, 'Vi phạm nhẹ, thiệt hại thấp → Phạt nhẹ'),
-- Bổ sung luật cho Violation
('violation', 'R7_Viol_Serious_All', '[{"variable":"severity","term":"serious"},{"variable":"violation_area","term":"large"},{"variable":"recidivism","term":"yes"},{"variable":"damage","term":"high"}]', 'heavy_penalty', 1.0, 14, 'Vi phạm rất nghiêm trọng, diện tích lớn, tái phạm, thiệt hại cao → Phạt tối đa'),
('violation', 'R8_Viol_Minor_Clean', '[{"variable":"severity","term":"minor"},{"variable":"violation_area","term":"small"},{"variable":"recidivism","term":"no"},{"variable":"duration","term":"short"}]', 'light_penalty', 0.9, 11, 'Vi phạm nhẹ, quy mô nhỏ, lần đầu, thời gian ngắn → Cảnh cáo'),
('violation', 'R9_Viol_Mod_Recidivism', '[{"variable":"severity","term":"moderate"},{"variable":"duration","term":"long"},{"variable":"damage","term":"medium"},{"variable":"recidivism","term":"once"}]', 'medium_penalty', 0.95, 14, 'Vi phạm vừa nhưng kéo dài và có tái phạm → Phạt trung bình cao'),
('violation', 'R10_Viol_Serious_Low_Damage', '[{"variable":"severity","term":"serious"},{"variable":"violation_area","term":"small"},{"variable":"recidivism","term":"no"},{"variable":"damage","term":"low"}]', 'medium_penalty', 0.8, 14, 'Hành vi nghiêm trọng nhưng chưa gây thiệt hại lớn → Phạt trung bình'),
('violation', 'R11_Viol_Mod_High_Damage', '[{"variable":"severity","term":"moderate"},{"variable":"violation_area","term":"large"},{"variable":"damage","term":"high"},{"variable":"recidivism","term":"no"}]', 'heavy_penalty', 0.85, 15, 'Vi phạm vừa nhưng quy mô và thiệt hại lớn → Phạt nặng'),
('violation', 'R12_Viol_Minor_Long_Dur', '[{"variable":"severity","term":"minor"},{"variable":"duration","term":"long"},{"variable":"damage","term":"medium"}]', 'medium_penalty', 0.75, 12, 'Vi phạm nhẹ nhưng để kéo dài gây thiệt hại trung bình → Phạt trung bình'),
('violation', 'R13_Viol_Minor_Large', '[{"variable":"severity","term":"minor"},{"variable":"violation_area","term":"large"},{"variable":"recidivism","term":"no"}]', 'medium_penalty', 0.7, 11, 'Hành vi nhẹ nhưng trên diện tích lớn → Phạt trung bình'),
('violation', 'R14_Viol_Mod_Short_Recid', '[{"variable":"severity","term":"moderate"},{"variable":"duration","term":"short"},{"variable":"damage","term":"low"},{"variable":"recidivism","term":"once"}]', 'medium_penalty', 0.65, 14, 'Vi phạm vừa, mới xảy ra nhưng có tái phạm → Phạt trung bình'),
('violation', 'R15_Viol_Serious_Short_Small', '[{"variable":"severity","term":"serious"},{"variable":"violation_area","term":"small"},{"variable":"duration","term":"short"}]', 'heavy_penalty', 0.75, 14, 'Hành vi nghiêm trọng dù quy mô nhỏ và mới → Phạt nặng'),
('violation', 'R16_Viol_Minor_High_Damage', '[{"variable":"severity","term":"minor"},{"variable":"damage","term":"high"},{"variable":"recidivism","term":"yes"}]', 'heavy_penalty', 0.8, 15, 'Hành vi nhẹ nhưng thiệt hại lớn và tái phạm → Phạt nặng'),
('violation', 'R17_Viol_Mod_Long_Low', '[{"variable":"severity","term":"moderate"},{"variable":"violation_area","term":"small"},{"variable":"duration","term":"long"},{"variable":"damage","term":"low"}]', 'medium_penalty', 0.6, 12, 'Vi phạm vừa, diện tích nhỏ nhưng kéo dài → Phạt trung bình'),
('violation', 'R18_Viol_Serious_Long_Once', '[{"variable":"severity","term":"serious"},{"variable":"duration","term":"long"},{"variable":"recidivism","term":"once"}]', 'heavy_penalty', 0.95, 14, 'Nghiêm trọng, kéo dài và tái phạm → Phạt rất nặng'),
('violation', 'R19_Viol_Minor_Med', '[{"variable":"severity","term":"minor"},{"variable":"violation_area","term":"medium"},{"variable":"damage","term":"medium"},{"variable":"recidivism","term":"no"}]', 'light_penalty', 0.5, 11, 'Vi phạm nhẹ, quy mô và thiệt hại trung bình → Phạt nhẹ'),
('violation', 'R20_Viol_Mod_Med_Once', '[{"variable":"severity","term":"moderate"},{"variable":"violation_area","term":"medium"},{"variable":"duration","term":"medium"},{"variable":"recidivism","term":"once"}]', 'heavy_penalty', 0.7, 14, 'Vi phạm vừa, quy mô trung bình và có tái phạm → Phạt nặng');

-- ============================================================
-- 11. Fuzzy Rules - Module: Tax (Thuế đất đai)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
('tax', 'R1_Tax_Preferential', '[{"variable":"location_type","term":"remote"},{"variable":"area_size","term":"within_limit"}]', 'preferential', 1.0, 1, 'Đất vùng sâu vùng xa, trong hạn mức -> Thuế ưu đãi'),
('tax', 'R2_Tax_Standard_Res', '[{"variable":"usage_purpose","term":"residential"},{"variable":"location_type","term":"rural"}]', 'standard', 0.9, 1, 'Đất ở nông thôn -> Tiêu chuẩn'),
('tax', 'R3_Tax_Standard_Urb', '[{"variable":"usage_purpose","term":"residential"},{"variable":"location_type","term":"urban"},{"variable":"area_size","term":"within_limit"}]', 'standard', 0.8, 1, 'Đất ở đô thị trong hạn mức -> Tiêu chuẩn'),
('tax', 'R4_Tax_High_OverLimit', '[{"variable":"usage_purpose","term":"residential"},{"variable":"area_size","term":"over_limit"}]', 'high_tax', 0.9, 1, 'Đất ở vượt hạn mức -> Thuế cao lũy tiến'),
('tax', 'R5_Tax_High_Com_Urb', '[{"variable":"usage_purpose","term":"commercial"},{"variable":"location_type","term":"urban"}]', 'high_tax', 1.0, 1, 'Đất thương mại đô thị -> Rất cao'),
('tax', 'R6_Tax_Med_Com_Rur', '[{"variable":"usage_purpose","term":"commercial"},{"variable":"location_type","term":"rural"}]', 'standard', 0.9, 1, 'Đất thương mại nông thôn -> Tiêu chuẩn (tương đối cao)'),
('tax', 'R7_Tax_High_Value_Urban', '[{"variable":"land_value","term":"high"},{"variable":"location_type","term":"urban"}]', 'high_tax', 1.0, 1, 'Đất giá trị cao ở đô thị -> Thuế cao'),
('tax', 'R8_Tax_Low_Value_Remote', '[{"variable":"land_value","term":"low"},{"variable":"location_type","term":"remote"}]', 'preferential', 0.9, 1, 'Đất giá trị thấp ở vùng sâu -> Ưu đãi');
