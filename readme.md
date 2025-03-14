# API Documentation

## Authentication
- POST `/auth/login`
- POST `/auth/register`

## Founder Endpoints

### Profile
- GET `/founder/profile/{founder_id}` - Get founder profile details

### Pitches
- GET `/founder/{founder_id}/pitches` - Get all pitches for a founder

### Questions & Answers
- GET `/founder/{founder_id}/pitches/{pitch_id}/questions` - Get all questions and answers for a pitch
- GET `/founder/{founder_id}/questions/unanswered` - Get all unanswered questions across pitches

### Documents
- POST `/founder/{founder_id}/pitches/{pitch_id}/documents` - Upload document to pitch
- GET `/founder/{founder_id}/pitches/{pitch_id}/documents` - Get all accessible documents

### Team Invites
- POST `/founder/{founder_id}/team/invite` - Invite member to founder team

### Offers
- GET `/founder/{founder_id}/pitches/{pitch_id}/offers` - Get all offers for a pitch
- POST `/founder/offers/{offer_id}/action` - Take action on offer (accept/reject)

### Bills
- GET `/founder/{founder_id}/pitches/{pitch_id}/bills` - Get all bills for a pitch

## Investor Endpoints

### Profile
- GET `/investor/investor/profile/{investor_id}` - Get investor profile

### Daftar Management
- GET `/investor/daftar/profile/{daftar_id}` - Get daftar profile
- GET `/investor/daftars/{daftar_id}/investors` - Get all investors in daftar
- POST `/investor/daftars/{daftar_id}/investors` - Add investor to daftar
- POST `/investor/daftars/{daftar_id}/invite` - Invite member to daftar

### Questions
- GET `/investor/scouts/{scout_id}/sample-questions` - Get sample questions
- POST `/investor/scouts/{scout_id}/custom-questions` - Create custom question
- GET `/investor/scouts/{scout_id}/custom-questions` - Get custom questions

### Documents
- POST `/investor/pitches/{pitch_id}/documents` - Upload document to pitch
- GET `/investor/pitches/{pitch_id}/documents` - Get accessible documents

### Offers
- POST `/investor/pitches/{pitch_id}/offers` - Create new offer
- GET `/investor/pitches/{pitch_id}/offers` - Get all offers for pitch
- POST `/investor/offers/{offer_id}/action` - Take action on offer (withdraw)

### Bills
- POST `/investor/pitches/{pitch_id}/bills` - Create new bill

## Models

### Document
- Pitch
- Scout
- Investor
- Founder
- Daftar
